using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace HighPoint.Models
{
    public class Article
    {
        public string url;
        public string title;
        public string author;
        public string body;
        public string sentiment;
        public Article(string u, string t, string a, string b, string s)
        {
            url = u;
            title = t;
            author = a;
            body = b;
            sentiment = s;
        }
    }
}
