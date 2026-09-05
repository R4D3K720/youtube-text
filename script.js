const button =
    document.getElementById("transcribeButton");

const input =
    document.getElementById("youtubeURL");

const loading =
    document.getElementById("loading");

const result =
    document.getElementById("result");

const transcript =
    document.getElementById("transcript");

const copyButton =
    document.getElementById("copyButton");


button.addEventListener("click", async () => {

    const url = input.value.trim();

    if (!url) {
        alert("Wklej link do filmu YouTube.");
        return;
    }


    loading.classList.remove("hidden");
    result.classList.add("hidden");


    try {

        const response = await fetch(
            "https://youtube-text-l8y1.onrender.com/transcribe",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    url: url
                })
            }
        );


        const data = await response.json();


        if (!response.ok) {
            throw new Error(
                data.detail || "Wystąpił błąd."
            );
        }


        transcript.textContent =
            data.transcript;


        loading.classList.add("hidden");
        result.classList.remove("hidden");


    } catch (error) {

        loading.classList.add("hidden");

        alert(
            "Błąd: " + error.message
        );

    }

});

copyButton.addEventListener("click", async () => {

    await navigator.clipboard.writeText(
        transcript.textContent
    );

    copyButton.textContent = "Skopiowano ✓";

    setTimeout(() => {
        copyButton.textContent = "Kopiuj";
    }, 1500);

});