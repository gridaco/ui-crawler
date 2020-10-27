const fs = require("fs");
const md5 = require("md5");
const sha1 = require("sha1");
const imageDownloader = require("node-image-downloader");

let data = fs.readFileSync("./data.json", "utf-8");
let array = JSON.parse(data).data;
let img_data = new Array();

for (i in array) {
  (function(x){
    setTimeout(function(){
      let uri = array[x].image_urls[0];
      imageDownloader({
        imgs: [
          {
            uri: uri,
            filename: sha1(uri),
          },
        ],
        dest: "./full", //destination folder
      })
      .then((info) => {
        console.log("all done", info);
        img_data.push(info);
        fs.writeFileSync("./result.json", JSON.stringify(img_data));
      })
      .catch((error, response, body) => {
        console.log("something goes bad!");
        console.log(error);
        img_data.push(error, response);

      fs.writeFileSync("./result.json", JSON.stringify(img_data));
    });
    }, 1000*x);
  })(i);
}
