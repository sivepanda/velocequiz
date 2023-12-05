<script lang="ts">
    // @ts-nocheck
    import axios, { formToJSON } from "axios";
    import Question from "../../components/Question.svelte";
	import Topic from "../../components/Topic.svelte";

    let files: FileList;
    let filename: string = '';
    let uploadFilename: string = '';
    let submitReady = false;
    let submitted = false;
    let topicsGenerated = false;
    let topics = []

    $: uploadFilename = files ? files.item('0').name : '';
    $: filename;
    $: submitReady = uploadFilename != '';
    $: topics;
    $: submitted;
    $: topicsGenerated;

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
            url: "http://127.0.0.1:5000/topics",
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
        filename = uploadFilename
        topics = response.data
    }
</script>

<body class="page">
    <h1>veloce<span class='logotype'>quiz</span></h1>
    
    <div class="uploads">
        
        <h1>Upload your PDF</h1>
        <label class="file-upload">
            <input type="file" id="file-upload" accept=".pdf" bind:files />
            <span class="material-symbols-outlined">
                upload_file
            </span>
        </label>
        <p>{uploadFilename}</p>

        <button class='{submitReady ? 'visible' : 'invisible'}' on:click={upload}>Submit</button>
        
        <lottie-player class="loading {submitted ? 'visible': 'invisible'}" src="https://lottie.host/d88782da-f3ef-4dad-9931-295644718e9a/uK2sClsyGy.json" background="#FFFFFF00" speed="1" style="width: 300px; height: 300px" loop autoplay direction="1" mode="normal"></lottie-player>
    
    </div>
    
    <div>
        <div class="questions {topicsGenerated ? 'visible' : 'invisible'}">
            <h1>Found Topics - <span>{filename}</span></h1>
            <Question showAnswer={false} questionNumber={1}></Question>
            {#each topics as topic}
                <Topic topic={topic}/>
                
            {/each}

        </div>
        
    
    </div>
</body>



<style>
    @import url('https://fonts.googleapis.com/css2?family=Dela+Gothic+One&family=Inter:wght@600&family=Open+Sans&display=swap');
    @media only print {
        .uploads {
            display: none;
            visibility: hidden;
            height: 0vh;
        }
        .questions {
            width: 90vw !important;

        }
        .questions h1 {
            font-size: 30px;
            padding: 0px;
            align-self: flex-start;
        }
        .sub {
            display: none;
            visibility: hidden;
        }
    }
    .uploads {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
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
    h1 > span {
        font-weight: 400;
    }
    button {
        width: 70%;
        justify-self: start;
    }
    .questions {
        margin-left: auto;
        margin-right: auto;
        width: 50vw;
    }
    input[type="file"], input[type="checkbox"] {
        display: none;
    }
    .sub {
        width: 50vw;
        display: grid;
        grid-template-columns: 1fr 1fr;
        flex-direction: row;
        gap: 4vw;
        align-items: center;
    }
    .showdiv {
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 10px;
        justify-self: end;
    }
    .show-answers {
        border-radius: 10px;
        height: 4.25svh;
        width: 4.25svh;
        margin: 2px;
        border: 2px solid black;
        background-color: var(--forest-200);
        color: var(--midnight-500);
        display: flex;
        align-items: center;
        justify-content: center;
        transition: 100ms all cubic-bezier(.12,.59,.85,.99);
    }
    .show-answers:hover {
        margin: 0px;
        border: 4px solid black;
        background-color: var(--forest-250);
        transition: 200ms all cubic-bezier(1,.39,.61,.96);
    }
    .show-answers span {
        font-size: 3svh;
        user-select: none;
    }
    .file-upload {
        border-radius: 10svh;
        height: 14svh;
        width: 14svh;
        margin: calc(.5svh + 5px);
        border: 5px solid black;
        background-color: var(--forest-200);
        color: var(--midnight-500);
        display: flex;
        align-items: center;
        justify-content: center;
        transition: 100ms all cubic-bezier(.12,.59,.85,.99);
    }
    .file-upload:hover {
        margin: calc(0svh + 0px);
        height: 15svh;
        width: 15svh;
        border: 10px solid black;
        background-color: var(--forest-250);
        transition: 200ms all cubic-bezier(1,.39,.61,.96);
    }
    .file-upload span {
        font-size: 8svh;
        user-select: none;
        transition: 100ms all cubic-bezier(.12,.59,.85,.99);
    }
    .file-upload:hover span {
        font-size: 7svh;
        transition: 200ms all cubic-bezier(1,.39,.61,.96);
    }

</style>