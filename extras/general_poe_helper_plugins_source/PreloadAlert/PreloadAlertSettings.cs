using System.Windows.Forms;
using ExileCore.Shared.Interfaces;
using ExileCore.Shared.Nodes;
using SharpDX;
using ImGuiNET;

namespace PreloadAlert
{
    public class PreloadAlertSettings : ISettings
    {
        public PreloadAlertSettings()
        {
            Enable = new ToggleNode(true);
            BackgroundColor = new ColorBGRA(0, 0, 0, 255);
            DefaultTextColor = new ColorBGRA(210, 210, 210, 255);
            ReloadKey = new HotkeyNode(Keys.F5);

            ServerAddress = new TextNode("");
            RequestTimeout = new TextNode("2");
        }

        public ToggleNode Enable { get; set; }
        public ColorNode BackgroundColor { get; set; }
        public ColorNode DefaultTextColor { get; set; }
        public HotkeyNode ReloadKey { get; set; }
        public TextNode ServerAddress { get; set; }
        public TextNode RequestTimeout { get; set; }

    }
}
