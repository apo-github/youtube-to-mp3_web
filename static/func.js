//初期ロード画面
window.onload = function() {
    const spinner = document.getElementById('loading');
    spinner.classList.add('loaded');
}

// //待機画面 
// jQuery(window).on("load", function() {
// 	// jQuery("body").attr("data-loading", "true");
//     const spinner = document.getElementById('loading');
//     spinner.classList.add('loaded');
// });

// URL確認処理
function clearText() {
	let url_form = document.getElementById("url");
    url_form.value = '';
}

function isValidUrl() {
    console.log("isValidUrl処理")
    let url_text = document.getElementById('url').value;
    
    try {
        new URL(url_text); 
        return true; 
    } catch (err) { 
        alert("Please enter a valid URL (´・ω・`)");
        clearText();
        return false; 
    }

}

function submitClick(){
    print("読まれたよ")
    let url_text = document.getElementById('url').value;
    if (url_text == null || url_text == "" || url_text.trim() === ""){//空白の場合
        alert("Please enter a valid URL (´・ω・`)");
        clearText();
        return false; 
    }else if (url_text.includes('@')){ //チャンネルの場合
        alert("Sorry, Channel URL is not available (´・ω・`)");
        clearText();
        return false; 
    }
}



let url = document.getElementById('url');
url.addEventListener('change', isValidUrl); // イベントが発生した時の処理

let submitButton = document.getElementById('submit');
submitButton.addEventListener('click', submitClick); //submitボタンが押された時の処理