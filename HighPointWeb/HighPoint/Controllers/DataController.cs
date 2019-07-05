using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using HighPoint.Models;


namespace HighPoint.Controllers
{
    [Route("api")]
    public class DataController : Controller
    {
        [HttpGet("dataList")]
        public List<Article> GetData()
        {
            DataReader r = new DataReader();
            return r.Populate();
        }
    }
}