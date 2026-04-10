const fromText = document.querySelector(".from-text"),
toText = document.querySelector(".to-text"),
selectTag = document.querySelectorAll("select"),
translateBtn = document.querySelector(".primary-btn"),
swapBtn = document.getElementById("swap-btn");

const languages = {
    "en-GB": "English",
    "hi-IN": "Hindi",
    "es-ES": "Spanish",
    "fr-FR": "French",
    "de-DE": "German",
    "ja-JP": "Japanese",
    "bho-BHO":"Bhojpuri"
};

selectTag.forEach((tag, id) => {
    for (let lang_code in languages) {
        let selected = id == 0 ? (lang_code == "en-GB" ? "selected" : "") : (lang_code == "hi-IN" ? "selected" : "");
        let option = `<option value="${lang_code}" ${selected}>${languages[lang_code]}</option>`;
        tag.insertAdjacentHTML("beforeend", option);
    }
});

// SWAP Logic
swapBtn.addEventListener("click", () => {
    let tempText = fromText.value;
    let tempLang = selectTag[0].value;
    fromText.value = toText.value;
    toText.value = tempText;
    selectTag[0].value = selectTag[1].value;
    selectTag[1].value = tempLang;
});

translateBtn.addEventListener("click", () => {
    let text = fromText.value.trim(),
    translateFrom = selectTag[0].value,
    translateTo = selectTag[1].value;
    if(!text) return;
    toText.placeholder = "Translating...";
    let apiUrl = `https://api.mymemory.translated.net/get?q=${text}&langpair=${translateFrom}|${translateTo}`;
    fetch(apiUrl).then(res => res.json()).then(data => {
        toText.value = data.responseData.translatedText;
        toText.placeholder = "Translation";
    });
});

document.getElementById("copy-btn").addEventListener("click", () => {
    navigator.clipboard.writeText(toText.value);
});