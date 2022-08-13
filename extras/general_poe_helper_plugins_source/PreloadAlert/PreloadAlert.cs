using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using ExileCore;
using ExileCore.Shared.Enums;
using ExileCore.Shared.Helpers;
using ImGuiNET;
using SharpDX;
using Vector2 = System.Numerics.Vector2;

using Newtonsoft.Json;

namespace PreloadAlert
{
    public class PreloadAlert : BaseSettingsPlugin<PreloadAlertSettings>
    {
        private string PreloadAlerts => Path.Combine(DirectoryFullName,"config","preload_alerts_default.txt");
        private string previousContent = null;
        private const int DefaultRequestTimeout = 2;
        private string PreloadAlertsPersonal => Path.Combine(DirectoryFullName, "config", "preload_alerts_personal.txt");
        private ConcurrentDictionary<string, PreloadConfigLine> PreloadConfigLines { get; } = new ConcurrentDictionary<string, PreloadConfigLine>();
        private ConcurrentDictionary<string, PreloadConfigLine> AlertsToDraw { get; } = new ConcurrentDictionary<string, PreloadConfigLine>();
        private Action<string, Color> AddPreload => ExternalPreloads;
        private List<string> PreloadDebug { get; } = new List<string>();
        private Action PreloadDebugAction { get; set; }

        public bool isTimeoutValid()
        {
            try
            {
                int.Parse(Settings.RequestTimeout);
                return true;
            }
            catch (Exception) {
                return false;
            }
        }

        public override void OnLoad()
        {
            ReadConfigFiles();
            Graphics.InitImage("preload-start.png");
            Graphics.InitImage("preload-end.png");
            Graphics.InitImage("preload-new.png");
        }

        public override bool Initialise()
        {
            GameController.PluginBridge.SaveMethod($"{nameof(PreloadAlert)}.{nameof(AddPreload)}", AddPreload);
            GameController.LeftPanel.WantUse(() => Settings.Enable);
            AreaChange(GameController.Area.CurrentArea);
            return true;
        }

        private void ReadConfigFiles()
        {
            if (!File.Exists(PreloadAlerts))
            {
                DebugWindow.LogError($"PreloadAlert.ReadConfigFiles -> Config file is missing: {PreloadAlerts}");
                return;
            }
            if (!File.Exists(PreloadAlertsPersonal))
            {
                File.Create(PreloadAlertsPersonal);
                DebugWindow.LogMsg($"PreloadAlert.ReadConfigFiles -> Personal config file got created: {PreloadAlertsPersonal}");
            }

            PreloadConfigLines.Clear();

            AddLinesFromFile(PreloadAlerts, PreloadConfigLines);
            AddLinesFromFile(PreloadAlertsPersonal, PreloadConfigLines);
        }

        private static void AddLinesFromFile(string path, IDictionary<string, PreloadConfigLine> preloadLines)
        {
            if (!File.Exists(path)) return;

            var lines = File.ReadAllLines(path);
            foreach (var line in lines)
            {
                if (string.IsNullOrWhiteSpace(line)) continue;
                if (line.StartsWith("#")) continue;

                var lineContent = line.Split(';');
                var metadataKey = lineContent[0].Trim();
                if (preloadLines.ContainsKey(metadataKey))
                {
                    if (line.StartsWith("-"))
                    {
                        preloadLines.Remove(metadataKey);
                    }
                    continue;
                }

                var textAndColor = new PreloadConfigLine
                {
                    Text = lineContent[1].Trim(),
                    Color = lineContent.ConfigColorValueExtractor(2)
                };
                preloadLines.Add(metadataKey, textAndColor);
            }
        }

        public override void AreaChange(AreaInstance area)
        {
            AlertsToDraw.Clear();
            PreloadDebugAction = null;
            Parse();
        }

        private void ExternalPreloads(string text, Color color)
        {
            AlertsToDraw.TryAdd(text, new PreloadConfigLine {Text = text, FastColor = () => color});
        }

        private void Parse()
        {
            PreloadDebug.Clear();
            try
            {
                GameController.Files.ReloadFiles();
                var allFiles = GameController.Files.AllFiles;
                foreach (var file in allFiles)
                {
                    if (file.Value.ChangeCount != GameController.Game.AreaChangeCount) continue;
                        
                    var text = file.Key;
                    if (string.IsNullOrWhiteSpace(text)) continue;
                    if (text.Contains('@')) text = text.Split('@')[0];

                    text = text.Trim();
                    PreloadDebug.Add(text);
                    CheckForPreload(text);                                
                }


            }
            catch (Exception e)
            {
                DebugWindow.LogError($"{nameof(PreloadAlert)} -> {e}");
            }
        }

        public override Job Tick()
        {
            if (Input.GetKeyState(Settings.ReloadKey.Value))
            {
                ReadConfigFiles();
                AreaChange(GameController.Area.CurrentArea);
            }
            return null;
        }

        private bool ShouldRender()
        {
            if (!Settings.Enable
                || GameController.Area.CurrentArea == null
                || GameController.Area.CurrentArea.IsTown
                || GameController.Area.CurrentArea.IsHideout
                || GameController.IsLoading
                || !GameController.InGame
                || GameController.Game.IngameState.IngameUi.StashElement.IsVisibleLocal
                )
            {
                return false;
            }

            var uiHover = GameController.Game.IngameState.UIHover;
            var miniMap = GameController.Game.IngameState.IngameUi.Map.SmallMiniMap;

            if (uiHover?.Tooltip != null 
                && uiHover.IsValid 
                && uiHover.Address != 0x00 
                && uiHover.Tooltip.Address != 0x00 
                && uiHover.Tooltip.IsVisibleLocal 
                && uiHover.Tooltip.GetClientRectCache.Intersects(miniMap.GetClientRectCache))
            {
                return false;
            }

            return true;
        }

        public override void Render()
        {
            PreloadDebugAction?.Invoke();

            if (!ShouldRender()) return;
            var startDrawPoint = GameController.LeftPanel.StartDrawPoint;
            var f = startDrawPoint.Y;
            var maxWidth = 0f;
            var lastLine = Vector2.Zero;

            var toDraw = AlertsToDraw
                .ToArray()
                .OrderBy(a => a.Value.Text);

            var contentString = "";
            List<string> content = new List<string>();

            foreach (var keyLinePair in toDraw)
            {
                var line = keyLinePair.Value;
                lastLine = Graphics.DrawText(
                    line.Text, 
                    startDrawPoint,
                    line.FastColor?.Invoke() ?? line.Color ?? Settings.DefaultTextColor, 
                    FontAlign.Right
                );
                contentString += line.Text;
                content.Add(line.Text.Replace("\"", ""));
                startDrawPoint.Y += lastLine.Y;
                maxWidth = Math.Max(lastLine.X, maxWidth);
            }

            if (
                Settings.ServerAddress != "" &&
                contentString != previousContent
            ) {

                LocationContent locationContent = new LocationContent();
                locationContent.content = content;
                locationContent.last_update = DateTime.Now.ToString();

                try
                {
                    Requests.ExecutePostRequest(
                        Requests.GetRequest(
                            Settings.ServerAddress,
                            isTimeoutValid() ? int.Parse(Settings.RequestTimeout) : DefaultRequestTimeout
                        ), JsonConvert.SerializeObject(locationContent, Formatting.Indented)
                    );
                }
                catch (Exception e)
                {
                    DebugWindow.LogError($"{nameof(PreloadAlert)} -> {e} \n\n\n {JsonConvert.SerializeObject(locationContent, Formatting.Indented)} \n\n\n");
                }
                previousContent = contentString;
            }

            var bounds = new RectangleF(GameController.LeftPanel.StartDrawPoint.X - maxWidth - 55,
                GameController.LeftPanel.StartDrawPoint.Y, maxWidth + 60, startDrawPoint.Y - f);

            Graphics.DrawImage("preload-new.png", bounds, Settings.BackgroundColor);
            GameController.LeftPanel.StartDrawPoint = startDrawPoint;
        }

        private void CheckForPreload(string text)
        {
            var preloadLine = PreloadConfigLines.FirstOrDefault(tuple => text == tuple.Key);
            if (preloadLine.Equals(default(KeyValuePair<string, PreloadConfigLine>))) return;

            AlertsToDraw.TryAdd(preloadLine.Key, preloadLine.Value);
        }

        public override void DrawSettings()
        {
            if (ImGui.Button("Dump preloads"))
            {
                Directory.CreateDirectory(Path.Combine(DirectoryFullName, "Dumps"));
                var path = Path.Combine(
                    DirectoryFullName,
                    "Dumps",
                    $"{GameController.Area.CurrentArea.Name}_{DateTime.Now.Ticks}.txt"
                    );
                File.WriteAllLines(path, PreloadDebug);
            }

            if (ImGui.Button("Dump grouped preloads"))
            {
                Directory.CreateDirectory(Path.Combine(DirectoryFullName, "Dumps"));
                var path = Path.Combine(
                    DirectoryFullName,
                    "Dumps",
                    $"{GameController.Area.CurrentArea.Name}_Grouped_{DateTime.Now.Ticks}.txt"
                    );
                File.WriteAllLines(path, PreloadDebug);
            }

            if (ImGui.Button("Show all preloads"))
            {
                var groupBy = PreloadDebug.OrderBy(x => x).GroupBy(x => x.IndexOf('/')).ToList();
                var result = new Dictionary<string, List<string>>(groupBy.Count);

                foreach (var gr in groupBy)
                {
                    var g = gr.ToList();

                    if (gr.Key != -1)
                    {
                        var list = new List<string>(g.Count);
                        result[g.First().Substring(0, gr.Key)] = list;

                        foreach (var str in g)
                        {
                            list.Add(str);
                        }
                    }
                    else
                    {
                        var list = new List<string>(g.Count);
                        var key = gr.Key.ToString();
                        result[key] = list;

                        foreach (var str in g)
                        {
                            list.Add(str);
                        }
                    }
                }

                groupBy = null;

                PreloadDebugAction = () =>
                {
                    foreach (var res in result)
                    {
                        if (ImGui.TreeNode(res.Key))
                        {
                            foreach (var str in res.Value)
                            {
                                ImGui.Text(str);
                            }

                            ImGui.TreePop();
                        }
                    }

                    ImGui.Separator();

                    if (AlertsToDraw.Count > 0)
                    {
                        if (ImGui.TreeNode("Alerts to draw"))
                        {
                            foreach (var keyAlertPair in AlertsToDraw)
                            {
                                var alert = keyAlertPair.Value;
                                ImGui.Text($"{alert.Text}");
                            }

                            ImGui.TreePop();
                        }
                    }

                    if (ImGui.Button("Close")) PreloadDebugAction = null;
                };
            }

            base.DrawSettings();
        }
    }
}
