using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Web;

namespace HighPoint.Models
{
    public class DataReader
    {
        public List<string[]> RawList = new List<string[]>();
        public List<Article> ArticleList = new List<Article>();

        public DataReader()
        {
            
        }

        private List<string[]> ParseFile()
        {

            StreamReader s = new StreamReader(File.OpenRead("/git/HighPoint/PythonScripts/out-2018-10-22--2018-10-29.txt"));
            string temp = "";
            while (!s.EndOfStream)
            {
                string[] article = new string[6];
                for(int i = 0; i < 6; i++)
                {
                    if (s.EndOfStream) { break;  }
                    temp = s.ReadLine();
                    article[i] = temp;
                }
                if (!s.EndOfStream) { temp = s.ReadLine(); }
                RawList.Add(article);
            }
            return RawList;
        } 

        public List<Article> Populate()
        {
            List<string[]> list = this.ParseFile();
            foreach (string[] i in list)
            {
                if (i[2] != null && !i[0].Equals(null) && i[2].Substring(0,2).Equals("An"))
                {
                    Article temp = new Article(
                    i[0].Substring(5),
                    "title here",
                    //i[3].Substring(7),
                    i[4].Substring(8),
                    "body here",
                    //i[5].Substring(6),
                    i[2].Substring(29, 6));
                    //Double.Parse(i[2].Substring(29, 6)));
                    ArticleList.Add(temp);
                }
            }
            return ArticleList;
        }
    }
}