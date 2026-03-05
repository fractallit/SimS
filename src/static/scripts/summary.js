document.getElementById('summary_form').addEventListener('submit', async function(e) {
    e.preventDefault();

    document.getElementById('result').textContent = "Summarizing...";

    const formData = new FormData(this);

    try {
        const response = await fetch('/summarize', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Error of server');
        }

        const result = await response.json();
        document.getElementById('result').textContent = result.result;
    } catch (error) {
        document.getElementById('result').textContent = 'Error: ' + error.message;
    }
});
