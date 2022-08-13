using System;
using System.Windows.Forms; 
using System.Collections.Generic;

using ExileCore;
using ExileCore.Shared;
using ExileCore.Shared.Cache;
using ExileCore.Shared.Enums;
using ExileCore.Shared.Helpers;

using SharpDX;
using Newtonsoft.Json;
using NumbericsVector2 = System.Numerics.Vector2;

namespace MiscInformation
{

    public class MiscInformation : BaseSettingsPlugin<MiscInformationSettings>
    {
        private string areaName = "";
        private string oldAreaName = "";
        private const int DefaultRequestTimeout = 2;

        private Dictionary<int, float> ArenaEffectiveLevels = new Dictionary<int, float>
        {
            {71, 70.94f},
            {72, 71.82f},
            {73, 72.64f},
            {74, 73.4f},
            {75, 74.1f},
            {76, 74.74f},
            {77, 75.32f},
            {78, 75.84f},
            {79, 76.3f},
            {80, 76.7f},
            {81, 77.04f},
            {82, 77.32f},
            {83, 77.54f},
            {84, 77.7f}
        };

        private RectangleF bounds = RectangleF.Empty;
        private TimeCache<bool> CalcXp;
        private bool CanRender;
        private DebugInformation debugInformation;
        private NumbericsVector2 drawTextVector2;
        private string fps = "";
        private string latency = "";
        private Vector2 leftEndVector2, rightEndVector2;
        private Vector2 leftPanelStartDrawPoint = Vector2.Zero;
        private RectangleF leftPanelStartDrawRect = RectangleF.Empty;
        private float maxX, maxY, percentGot;
        private double partytime = 4000;
        private string ping = "";
        private DateTime startTime, lastTime;
        private long startXp, getXp, xpLeftQ;
        private float startY;
        private double time;
        private string timeLeft = "";
        private TimeSpan timeSpan;
        private string xpReceivingText = "";

        public bool isTimeoutValid()
        {
            try
            {
                int.Parse(Settings.RequestTimeout);
                return true;
            }
            catch (Exception)
            {
                return false;
            }
        }


        public float GetEffectiveLevel(int monsterLevel)
        {
            return Convert.ToSingle(-0.03 * Math.Pow(monsterLevel, 2) + 5.17 * monsterLevel - 144.9);
        }

        public override void OnLoad()
        {
            Order = -50;
            Graphics.InitImage("preload-start.png");
            Graphics.InitImage("preload-end.png");
            Graphics.InitImage("preload-new.png");
        }

        public override bool Initialise()
        {
            Input.RegisterKey(Keys.F10);

            Input.ReleaseKey += (sender, keys) =>
            {
                if (keys == Keys.F10) Settings.Enable.Value = !Settings.Enable;
            };

            GameController.LeftPanel.WantUse(() => Settings.Enable);
            CalcXp = new TimeCache<bool>(() =>
            {
                partytime += time;
                time = 0;
                var areaCurrentArea = GameController.Area.CurrentArea;

                if (areaCurrentArea == null)
                    return false;

                timeSpan = DateTime.UtcNow - areaCurrentArea.TimeEntered;

                maxX = MathHepler.Max(
                    Graphics.MeasureText(fps).X, 
                    Graphics.MeasureText(ping).X, 
                    Graphics.MeasureText(latency).X,
                    Graphics.MeasureText(areaName).X, 
                    Graphics.MeasureText(xpReceivingText).X, 
                    Graphics.MeasureText(timeLeft).X
               ) * Settings.WidthMultiplier;

                return true;
            }, 1000);

            debugInformation = new DebugInformation("Game FPS", "Collect game fps", false);
            return true;
        }

        public override Job Tick()
        {
            TickLogic();
            return null;
        }

        private void TickLogic()
        {
            time += GameController.DeltaTime;
            var gameUi = GameController.Game.IngameState.IngameUi;

            if (GameController.Area.CurrentArea == null || gameUi.InventoryPanel.IsVisible || gameUi.BetrayalWindow.IsVisibleLocal)
            {
                CanRender = false;
                return;
            }

            var UIHover = GameController.Game.IngameState.UIHover;

            if (UIHover.Tooltip != null && UIHover.Tooltip.IsVisibleLocal &&
                UIHover.Tooltip.GetClientRectCache.Intersects(leftPanelStartDrawRect))
            {
                CanRender = false;
                return;
            }

            CanRender = true;

            var ingameStateCurFps = GameController.Game.IngameState.CurFps;
            debugInformation.Tick = ingameStateCurFps;
            areaName = $"{GameController.Area.CurrentArea.DisplayName}";

            if (
                Settings.ServerAddress != "" &&
                areaName != oldAreaName
            ) {

                CurrentLocation currentLocation = new CurrentLocation();
                currentLocation.current_location = areaName;

                try
                {
                    Requests.ExecutePostRequest(
                        Requests.GetRequest(
                            Settings.ServerAddress,
                            isTimeoutValid() ? int.Parse(Settings.RequestTimeout) : DefaultRequestTimeout
                        ), JsonConvert.SerializeObject(currentLocation, Formatting.Indented)
                    );
                }
                catch (Exception e)
                {
                    DebugWindow.LogError($"{nameof(MiscInformation)} -> {e} \n\n\n {JsonConvert.SerializeObject(currentLocation, Formatting.Indented)} \n\n\n");
                }
                oldAreaName = areaName;
            }
        }

        public override void Render()
        {
            if (!CanRender)
                return;

            leftPanelStartDrawPoint = GameController.LeftPanel.StartDrawPoint;

            if (GameController.IngameState.IngameUi.Sulphit.IsVisible)
                leftPanelStartDrawPoint.X -= GameController.IngameState.IngameUi.Sulphit.Width;

            leftPanelStartDrawRect = new RectangleF(leftPanelStartDrawPoint.X, leftPanelStartDrawPoint.Y, 1, 1);

            leftPanelStartDrawPoint.X -= maxX;
            startY = leftPanelStartDrawPoint.Y;
            leftPanelStartDrawPoint.Y += drawTextVector2.Y;
            leftPanelStartDrawPoint.Y += drawTextVector2.Y;
            leftPanelStartDrawPoint.Y += drawTextVector2.Y;
            leftEndVector2 = leftPanelStartDrawPoint;
            leftPanelStartDrawPoint.X += maxX;
            leftPanelStartDrawPoint.Y = startY;

            //NameArea
            drawTextVector2 = Graphics.DrawText(
                areaName, 
                leftPanelStartDrawPoint, 
                GameController.Area.CurrentArea.AreaColorName,
                FontAlign.Right
            );

            rightEndVector2 = leftPanelStartDrawPoint;
            var max = Math.Max(rightEndVector2.Y, leftEndVector2.Y + 5);
            bounds = new RectangleF(leftEndVector2.X, startY - 2, rightEndVector2.X - leftEndVector2.X, max);

            Graphics.DrawImage("preload-new.png", bounds, Settings.BackgroundColor);
            GameController.LeftPanel.StartDrawPoint = new Vector2(leftPanelStartDrawPoint.X, max + 10);
        }
    }
}
