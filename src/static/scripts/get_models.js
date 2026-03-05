const parent = document.getElementById('select_llm_model');

async function getModels() {
    parent.innerHTML = '';

    var answer = await fetch('/get_ollama_tags').catch(function(err) {
        console.log(err);
        parent.innerHTML = '<option value="Error">Please check your llama server</option>';
        return;
    });

    var data = await answer.json();

    for (var i = 0; i < data.models.length; i++) {
        var model_name = data.models[i].name;

        parent.innerHTML += '<option value="' + model_name + '">' + model_name + '</option>';
    }
}

