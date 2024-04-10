function doPost(e) {
    // 最初のシートを取得
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
    // 受信したJSONデータの情報をシートの末尾に行を追加
    var params = JSON.parse(e.postData.contents);
    sheet.appendRow([new Date().toLocaleString('ja-JP'),
        params.temperature, params.humidity, params.moisture]);
        // クライアントへの応答を構築
    const output = ContentService.createTextOutput(JSON.stringify({result:"Ok"}));
    output.setMimeType(ContentService.MimeType.JSON);
    return output;
}

