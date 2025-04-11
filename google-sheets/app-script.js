function doPost(e) {
  try {
    var sheet = SpreadsheetApp.openById("1DyP02BKG6KXA_5U8lxiHx39jgq4A_-PstQJDpzMrCKw").getSheets()[0];
    var data = JSON.parse(e.postData.contents);
    sheet.appendRow([new Date(), data.distance]);
    return ContentService.createTextOutput("OK");
  } catch (err) {
    return ContentService.createTextOutput("Error: " + err);
  }
}

function doGet(e) {
  try {
    var sheet = SpreadsheetApp.openById("1DyP02BKG6KXA_5U8lxiHx39jgq4A_-PstQJDpzMrCKw").getSheets()[0];
    var lastRow = sheet.getLastRow();
    var lastDistance = sheet.getRange(lastRow, 2).getValue();
    return ContentService.createTextOutput("Last Distance: " + lastDistance);
  } catch (err) {
    return ContentService.createTextOutput("Error: " + err);
  }
}
