function clearText() {
	var url_form = document.getElementById("url");
    url_form.value = '';
}

function isValidUrl() {
    console.log("isValidUrl処理")
    let url_text = document.getElementById('url').value;
    
    try {
        new URL(url_text); 
        return true; 
    } catch (err) { 
        alert("Please enter a valid URL(´・ω・`)");
        clearText();
        return false; 
    }

}

function submitClick(){
    let url_text = document.getElementById('url').value;
    if (url_text == null || url_text == "" || url_text.trim() === ""){
        alert("Please enter a valid URL(´・ω・`)");
        clearText();
        return false; 
    }
}

let url = document.getElementById('url');
url.addEventListener('change', isValidUrl); // イベントが発生した時の処理

let submitButton = document.getElementById('submit');
checkButton.addEventListener('click', submitClick); //submitボタンが押された時の処理