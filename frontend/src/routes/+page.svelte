<script lang="ts">
    // @ts-nocheck
    import axios, { formToJSON } from "axios";
    import Question from "../components/Question.svelte";

    let files: FileList;
    let filename: string = '';
    let questions = []
    let questionNumber = 0;
    let submitReady = false;
    let submitted = false;
    let questionsGenerated = false;

    $: filename = files? files.item('0').name : '';
    $: submitReady = filename != '';
    $: questions;
    $: submitted;
    $: questionsGenerated;

    const upload = async () => {
        if(!files) {
            console.log('nothing')
            return
        }
        submitted = true;
        console.log(files.item("0"))
        var file:File = files.item("0");
        const formData = axios.toFormData({"file": file});

        const response = await axios({
            method: "post",
            url: "http://127.0.0.1:5000/upload",
            data: formData,
            headers: {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "multipart/form-data"
            }
        })
        
        console.log(response.data)
        submitted = false
        questionsGenerated = true
        files = null
        questions = response.data

        // response.data.forEach(question => {
        //     questions.push(question.replace(/(?:\r\n|\r|\n)/g, '<br>'));
        //     console.log(question)
        // });
        
    }

</script>

<body class="page">
    <h1><span class='logotype'>quiz</span>ify</h1>
    <h1>Upload your PDF</h1>
    <label class="file-upload">
        <input type="file" id="file-upload" accept="pdf" bind:files />
        <span class="material-symbols-outlined">
            upload_file
        </span>
    </label>
    <p>{filename}</p>

    <button class='{submitReady ? 'visible' : 'invisible'}' on:click={upload}>Submit</button>
    
    <lottie-player class="loading {submitted ? 'visible': 'invisible'}" src="https://lottie.host/d88782da-f3ef-4dad-9931-295644718e9a/uK2sClsyGy.json" background="#FFFFFF00" speed="1" style="width: 300px; height: 300px" loop autoplay direction="1" mode="normal"></lottie-player>
    
    <div>
        <div class="questions {questionsGenerated ? 'visible' : 'invisible'}">
            <h1>Generated Questions</h1>
            <!-- <Question questionNumber={(questionNumber += 1)}></Question>
            <Question questionNumber={(questionNumber += 1)}></Question>
            <Question questionNumber={(questionNumber += 1)}></Question>
            <Question questionNumber={(questionNumber += 1)}></Question> -->
            {#each questions as question}
                {#if question != "null"}
                    <Question question={question} questionNumber={(questionNumber += 1)}></Question>
                {/if}
            {/each}
        </div>
        
    
    </div>
</body>



<style>
    @import url('https://fonts.googleapis.com/css2?family=Dela+Gothic+One&family=Inter:wght@600&family=Open+Sans&display=swap');
    .logotype {
        font-family: 'Dela Gothic One', sans-serif;
        color: var(--forest-200) 
    }
    .page {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .loading {
        filter: hue-rotate(220deg) saturate(.22);
    }
    h1 {
        font-size: 5vh;
    }
    .questions {
        margin-left: auto;
        margin-right: auto;
        width: 50vw;
    }
    input[type="file"] {
        display: none;
    }
    .file-upload {
        margin: .5svh;
        height: 14svh;
        width: 14svh;
        border: 5px solid black;
        border-radius: 10svh;
        background-color: var(--forest-200);
        color: var(--midnight-500);
        display: flex;
        align-items: center;
        justify-content: center;
        transition: 100ms all cubic-bezier(.12,.59,.85,.99);
    }
    .file-upload:hover {
        margin: 0svh;
        height: 15svh;
        width: 15svh;
        background-color: var(--forest-250);
        transition: 200ms all cubic-bezier(1,.39,.61,.96);
    }
    .file-upload span {
        font-size: 8svh;
        transition: 100ms all cubic-bezier(.12,.59,.85,.99);
    }
    .file-upload:hover span {
        font-size: 7svh;
        transition: 200ms all cubic-bezier(1,.39,.61,.96);
    }

</style>