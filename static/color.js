document.addEventListener('DOMContentLoaded', function() {
    function searchWord() {
        var result = document.getElementById('result').innerText;
        var True = true;
        var False = false;
        var None = null
        console.log(result)
        var resultValue = eval('(' + result + ')');
        
        var paragraph = document.getElementById('oldParagraph');
        var content = paragraph.innerHTML;
        var newParagraph = document.getElementById('newParagraph');
        var fixContent = newParagraph.innerHTML;

        for (var key in resultValue) {
            var suggestion = resultValue[key].suggestion;
            var is_correct = resultValue[key].is_correct;
            if (is_correct) {
                content = content.replace(new RegExp(key, 'g'), '<span class="font-bold text-green-500">$&</span>');
                fixContent = fixContent.replace(new RegExp(key, 'g'), '<span class="font-bold text-green-500">$&</span>');
            } else {
                content = content.replace(new RegExp(key, 'g'), '<span class="font-bold text-red-500">$&</span>');
                fixContent = fixContent.replace(new RegExp(key, 'g'), '<span class="font-bold text-blue-700">' + suggestion + '</span>');
            }
        }
    
        paragraph.innerHTML = content;
        newParagraph.innerHTML = fixContent;
    }

    searchWord(); // Call searchWord function when the page loads
});