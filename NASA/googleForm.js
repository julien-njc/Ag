// var ssID = "13-hAZ_zYZpFLSbikaNqvoie4F7ofwMPWCEg40SVc44g"; // sheet 1
// var ssID = "1_zzn0lajHnxW7QvgBbFbx_J2jReTHkYXZR5pJMbxEBA"; // sheet 2
// var ssID = "1f2bZKaOAWHzOEmAKeSOT4RZJQXSQiTW35djcWwpEkv8"; // sheet 3
// var ssID = "17W4-5w5hhe1MFZZhIPVndIQ4k_2zXt_M7fGBkdR9764";//sheet4
// var ssID = "1IBu7MzZmq1Ocw04h3foGBguCC8D0l8llHVudrkGDwqA";//sheet5
// var ssID = "1TVWzv3Q4y5fEDf1q38XY7HTei9OCtJ_KVcy1MQMcA88"; //sheet6
// var ssID = "1noIIVEGtsIK9XD8JYwHGDHeRAxTqZjFYZAJcontESMo" //sheet7
// var ssID = "1Ie1f7dE523txjQNL1XW7FJiXdpkKDeblVLnm2p35Ix4" //sheet8
// var ssID = "1cTWpl6Gx5JyHHIjTXUEAfvKaJiofFyt9Yw4E25PXZoE" //sheet9
// var ssID = "1skWow25KH1ldrNWZdfevbfNEzAV86gxPNeR5aHL0g0U" //sheet10
var ssID = "1qG1kf5Q2YFyIc_q840Xtq-Zhqfy06ozaXBezDgvukRM"

// var ssID = "11BQo8Nnjq6l34WeuViWW5afNXG9DZuXthjOw87CBvbo"; //1r6rLmbqt-M5Z3AZFsj1ci1ZReTLj3QFX5DPW_htS6L4

// var formID = "1Xv76C8CNU_hWPp0TxjCTmGOLl8l-WyzCKqxybnS7iqE";
// var formID = "12s_F0d5rxaknke05r_QSbPQV_FL3IkhCQz2Pgfddn9o"; //set 1
// var formID = "1TjlJ6yhlk26xKVwVwk9jcg6FbpzkezezYzJoDB8MxXw"; //set 2
// var formID = "1feSI_V92hI5z_lP_yfFHg8TYJFZvYx9ycGa5A71Y0ec"; //set 3
// var formID = "1WTu2Gpt3X5z36EjYMUitfogWqzeqlTyWLYZSwb13YGw"; //set 4
// var formID = "1U-ouwgRo6rkrRtp1S56QVq9mcSEC5eiINRm4mu0Wgow"; //set 5
// var formID = "1GoRMfuQub0R_5jofpfiDmz9UzGw-pfSAjR6kkxpARmM"; //set 6
// var formID = "1cdavyk3xyRGhCMr_K3Qxw2WxV-zWPa6TSTlKHlUxU3o"; //set 7
// var formID = "1i9BN8XRvjapYaqitRd3kBLnvVGSgH5KPLAEnm0OYrDc"; //set 8
// var formID = "1DEuP_-38mQmXiXpCVl76zigzKiQOom9XUpLvc5KLjIU"; //set 9
// var formID = "1TDaWowI01fFGYI1KwA2VdI6Rv51oYEt-K_D56VAsrEY"; //set 10
var formID = "16N_WsmArmuwY6zha99fKE-3cwLYdAKG0wVmUjrHDRUc"

var form = FormApp.openById(formID);
var wsdata = SpreadsheetApp.openById(ssID).getSheetByName("Sheet1").getDataRange().getValues();

function myFunction() {
  var image1_name = "";
  var image2_name = "";
  var files = "";
  var file = "";
  var image_split_arr = "";
  var img = "";

  wsdata.forEach(function (data, i) {

    files = DriveApp.getFilesByName(data[3]);
    while (files.hasNext()) {
      file = files.next();
      image1_name = file.getUrl();
      // Logger.log(i+"Img1"+image1_name);
      image_split_arr = image1_name.split("/");
      img = DriveApp.getFileById(image_split_arr[5]);
      form.addImageItem()
        .setImage(img);
    }

// http://www.google.com/maps/place/"+data[6]+","+data[7]+"/@"+data[6]+","+data[7]+",14z/data=!3m1!1e3")
      // http://www.google.com/maps/place/46.8327393,-118.9120915/@46.8327393,-118.9120915,14z/data=!3m1!1e3
      // https://www.google.com/maps/@"+data[6]+","+data[7]+",14z/data=!3m1!1e3")

    // Logger.log(data)
    if (i > 0) {
      var item1 = form.addMultipleChoiceItem();
      item1.setTitle("QUESTION " + data[0] + ": How would you classify? \n http://www.google.com/maps/place/"+data[6]+","+data[7]+"/@"+data[6]+","+data[7]+",14z/data=!3m1!1e3")
        .setChoices([
          item1.createChoice('Single Crop'),
          item1.createChoice('Double Crop/Cover crop'),
          item1.createChoice('Unsure')
        ]);

        var item2 = form.addMultipleChoiceItem();
      item2.setTitle("QUESTION: If double/cover crop, can you distinguish?")
        .setChoices([
          item2.createChoice('Unsure'),
          item2.createChoice('Double Crop'),
          item2.createChoice('Cover Crop'),
          
          
        ]);

        var comments = form.addParagraphTextItem();
        comments.setTitle('Comments');
    }

    

    files = DriveApp.getFilesByName(data[4]);
    while (files.hasNext()) {
      file = files.next();
      image1_name = file.getUrl();
      // Logger.log(i+"Img1"+image1_name);
      image_split_arr = image1_name.split("/");
      img = DriveApp.getFileById(image_split_arr[5]);
      form.addImageItem()
        .setImage(img);
    }


    form.addPageBreakItem()
  });
}