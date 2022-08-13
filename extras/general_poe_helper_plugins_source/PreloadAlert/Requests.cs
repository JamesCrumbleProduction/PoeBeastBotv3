using System.IO;
using System.Text;
using System.Net;

class Requests
{
    public static WebRequest GetRequest(string url, int timeout)
    {
        WebRequest request = WebRequest.Create(url);
        request.Timeout = timeout * 1000;

        return request;
    }

    public static string ExecuteGetRequest(WebRequest request)
    {
        string responseString = "";
        Stream responseStream = request.GetResponse().GetResponseStream();

        while (true)
        {

            int readedByte = responseStream.ReadByte();

            if (readedByte == -1)
            {
                break;
            }

            responseString += (char)readedByte;
        }
        responseStream.Close();

        return responseString;
    }
    public static void ExecutePostRequest(WebRequest request, string jsonData)
    {
        request.Method = "POST";

        byte[] byteArray = Encoding.UTF8.GetBytes(jsonData);

        request.ContentType = "application/json";
        request.ContentLength = byteArray.Length;

        Stream dataStream = request.GetRequestStream();
        dataStream.Write(byteArray, 0, byteArray.Length);
        dataStream.Close();

        request.GetResponse().Close();
    }
}