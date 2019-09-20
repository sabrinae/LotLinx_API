function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('GET REPORTS')
    .addItem('Get LL Campaign Data', 'getLLService')
    .addItem('Make Report Copy', 'backlog')
    .addToUi();
}

function getLLService() {
  var user = 'your email/username';
  var pwd = 'your password';
  var method = 'login';
  
  // in Postman, this is placed in the Body - since that's not really an option for GAS, we'll use POST method with payload
  var headers = {
    "method": method,
    "user": user,
    "pwd": pwd
  };
  
  var options = {
    payload: JSON.stringify(headers),
    contentType: "application/json",
    muteHttpExceptions: true
  };
  
  var loginUrl = 'https://turnapi-production.lotlinx.com/account.jsp';
  var url = loginUrl;
  
  var response = UrlFetchApp.fetch(url, options).getContentText();

  var initialData = JSON.parse(response);
  var token = initialData.token;
  
  lotLinxDataGrab(token);
}

function lotLinxDataGrab(token) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet1 = ss.getSheetByName('LotLinx Campaigns').activate();
  var sheet2 = ss.getSheetByName('formatting').activate();
  
  var currentMonth = sheet1.getRange(1, 1).getValue();
  
  var apiUrl = 'https://turnapi-production.lotlinx.com/reseller.jsp';
  
  var payload = {
    token: token,
    timeperiod: currentMonth,
    method: "summaryReport"
  };
  
  var params = {
    payload: JSON.stringify(payload),
    contentType: "application/json",
    method: "POST",
    muteHttpExceptions: true
  };
  
  var response = UrlFetchApp.fetch(apiUrl, params);
  
  if (response.getResponseCode() != 200) {
    Logger.log('Error ' + response.getResponseCode());
  } else {
    var llData = JSON.parse(response.getContentText());
    
    var row1 = [];
    var row2 = [];
    
    // first loop - data for sheet 2, 'LotLinx Totals'
    for (var key in llData.dealers) {
      var dealer = llData.dealers[key].dealerName;
      var totalBudgetDelivered = llData.dealers[key].totalBudgetDelivered;
      var totalShoppers = llData.dealers[key].totalShoppersDelivered;
      var percentNewToSite = llData.dealers[key].percentNewToSite;
      var totalVinsReached = llData.dealers[key].totalVinsReached;
      var totalVinsSold = llData.dealers[key].totalVinsSold;
      
      row2.push([dealer, totalBudgetDelivered, totalShoppers, percentNewToSite, totalVinsReached, totalVinsSold]);
      
      var key2 = 0;
      for (key2 in llData.dealers[key].campaigns) {
        var dealerName = llData.dealers[key].campaigns[key2].dealerName;
        var campaign = llData.dealers[key].campaigns[key2].campaignName;
        //Logger.log(campaign);
        var budgetDelivered = llData.dealers[key].campaigns[key2].budgetDelivered;
        var shoppersDelivered = llData.dealers[key].campaigns[key2].shoppersDelivered;
        var vinsDelivered = llData.dealers[key].campaigns[key2].vinsReached;
        var shoppersPerVin = llData.dealers[key].campaigns[key2].shoppersPerVin;
        var vinsSold = llData.dealers[key].campaigns[key2].vinsSold;
        key2++;
      
        row1.push([dealerName, campaign, budgetDelivered, shoppersDelivered, vinsDelivered, shoppersPerVin, vinsSold]);
        Logger.log(row1);
      } 
    }
    sheet1.getRange(4, 2, row1.length, row1[0].length).setValues(row1);
    
    var sheet3 = ss.getSheetByName('LotLinx Totals').activate();
    sheet3.getRange(2, 2, row2.length, row2[0].length).setValues(row2);
  }
}

function backlog() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var date = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "MMMM-dd-YYYY");
  var ssName = date + " " + ss.getName();
  
  var ogSSName = ss.getName();
  var backupSheet = DriveApp.getFilesByName(ogSSName);
  
  var destFolder = DriveApp.getFoldersByName('LotLinx Reports').next();
  DriveApp.getFileById(ss.getId()).makeCopy(ssName, destFolder);
}
