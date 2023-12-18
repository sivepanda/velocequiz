<script lang="ts">
    // @ts-nocheck
    import { quizzes } from '$lib/StoreQuiz';
    import axios, { formToJSON } from 'axios';
    import Question from '../../components/Question.svelte';
    import Topic from '../../components/Topic.svelte';

    let files: FileList;
    let filename: string = '';
    let uploadFilename: string = '';
    let submitReady = false;
    let submitted = false;
    let topicsGenerated = false;
    let topics = [];

    $: uploadFilename = files ? files.item('0').name : '';
    $: filename;
    $: submitReady = uploadFilename != '';
    $: topics;
    $: submitted;
    $: topicsGenerated;

    const upload = async () => {
        if (!files) {
            console.log('nothing');
            return;
        }

        submitted = true;
        console.log(files.item('0'));
        var file: File = files.item('0');
        const formData = axios.toFormData({ file: file });

        const response = await axios({
            method: 'post',
            url: 'http://127.0.0.1:5000/topics',
            data: formData,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'multipart/form-data'
            }
        });

        console.log(response.data);
        submitted = false;
        topicsGenerated = true;
        files = null;
        filename = uploadFilename;
        topics = response.data;
    };

    class ExtractedTopic {
        constructor(name, text) {
            this.name = name;
            this.text = text;
            this.numQuestions = 1;
        }
        setNumQuestion(num: number) {
            num = num >= 0 ? num : this.numQuestions;
            this.numQuestions = num;
        }
    }

    topics = [
        {
            name: 'Cybersecurity and hacking',
            text: 'Identify the loss of: Confidentiality, Integrity, -- Availability -- Confidentiality and Integrity. -- Names, Birth dates, Medical -- IDs/Social Security Numbers, -- Employment/Income Data, Street -- Addresses, and Email Addresses -- were all stolen by the hacker.Intent of Attack: -- (disclose, deceive, disrupt, destruct, usurp) -- This was an attack by a nation-state -- hacker, who works directly for a foreign -- nation. The intent could have been to -- disclose or disrupt depending on the -- nation that was responsible, the two main -- suspects were Russia and China. Although -- no actual medical information like test -- results or conditions were stolen, China -- could use the info for economic purposes -- with its large biotech industry. Russia -- could use the information of political -- officials as leverage in some political -- settings.'
        },
        {
            name: 'Cybersecurity Attack Phishing',
            text: 'Describe the Attack Environment -- The attack occurred via phishing on an employee, targeting their -- login and account. From there, the attackers used the login -- credentials to gain access to the network and from there were able -- to gain access to 90 additional systems from 50 accounts, -- eventually gaining access to a data warehouse, where they could -- read information about employees.Resources of the attacker -- The attackers simply needed a computer to -- send out phishing emails with a hyperlink -- containing malware to employees working -- at Anthem. Who ever downloaded it would -- allow the attacker to gain remote access -- to the computer and files.'
        },
        {
            name: 'Security Measures Effectiveness',
            text: 'Were there any controls or security measures in place? -- There were many standard security measures in place. They included: -- ● 2FA -- ● Enhanced Logging resources -- ● Changing passwords of privileged accounts -- ● New network admin IDs -- ● new incident management solutions -- Not all of these methods are completely effective, especially when it -- comes to attacks like phishing, that don’t rely on system faults but -- human faults.'
        }
    ];
    $: topics;
    $: console.log('lorem',topics);

    const create = async () => {
        console.log("Sending Topics")
        if (!topics) {
            console.log('nothing');
            return;
        }

        const response = await axios({
            method: 'post',
            url: 'http://127.0.0.1:5000/topic_quiz',
            data: topics,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            }
        });

        console.log(response.data);
        // submitted = false;
        // topicsGenerated = true;
        // files = null;
        // filename = uploadFilename;
        // topics = response.data;
    }
</script>

<body class="page">
    <a href="/" class="titlenm">veloce<span class="logotype">quiz</span></a>

    <div class="uploads">
        <h1>Upload your PDF</h1>
        <label class="file-upload">
            <input type="file" id="file-upload" accept=".pdf" bind:files />
            <span class="material-symbols-outlined"> upload_file </span>
        </label>
        <p>{uploadFilename}</p>

        <button class={submitReady ? 'visible' : 'invisible'} on:click={upload}>Submit</button>

        <lottie-player
            class="loading {submitted ? 'visible' : 'invisible'}"
            src="https://lottie.host/d88782da-f3ef-4dad-9931-295644718e9a/uK2sClsyGy.json"
            background="#FFFFFF00"
            speed="1"
            style="width: 300px; height: 300px"
            loop
            autoplay
            direction="1"
            mode="normal"
        />
    </div>

    <div>
        <div class="topics {topicsGenerated ? 'visible' : 'visible'}">
            <h1>Found Topics - <span>{filename}</span></h1>
            <p>
                These are the topics VeloceQuiz has found in your notes! Please select how many questions in
                each topic you would like in your quiz!
            </p>
            <div class="topiclist">
                {#each topics as topic}
                    <Topic topicName={topic.name} topicText={topic.text} bind:value="{topic}"/>
                {/each}
                <button on:click={create}>Create Quiz</button>
            </div>
        </div>
    </div>
</body>

<style>
    @import url('https://fonts.googleapis.com/css2?family=Dela+Gothic+One&family=Inter:wght@600&family=Open+Sans&display=swap');
    .uploads {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .logotype {
        font-family: 'Dela Gothic One', sans-serif;
        color: var(--forest-200);
    }
    .page {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .loading {
        filter: hue-rotate(220deg) saturate(0.22);
    }
    h1 {
        font-size: 5vh;
    }
    button {
        width: 70%;
        cursor: pointer;
        justify-self: start;
    }
    .topics {
        margin-left: auto;
        margin-right: auto;
        width: 50vw;
    }
    .topiclist {
        display: grid;
        width: 50vw;
        grid-template-columns: 1fr 1fr;
        align-items: center;
        justify-items: center;
    }
    .topiclist > button {
        grid-column: 1 / span 2;
        width: 40%;
        align-self: center;
        justify-self: center;
    }
    input[type='file'] {
        display: none;
    }
    .file-upload {
        cursor: pointer;
        border-radius: 10svh;
        height: 14svh;
        width: 14svh;
        margin: calc(0.5svh + 5px);
        border: 5px solid black;
        background-color: var(--forest-200);
        color: var(--midnight-500);
        display: flex;
        align-items: center;
        justify-content: center;
        transition: 100ms all cubic-bezier(0.12, 0.59, 0.85, 0.99);
    }
    .file-upload:hover {
        margin: calc(0svh + 0px);
        height: 15svh;
        width: 15svh;
        border: 10px solid black;
        background-color: var(--forest-250);
        transition: 200ms all cubic-bezier(1, 0.39, 0.61, 0.96);
    }
    .file-upload span {
        font-size: 8svh;
        user-select: none;
        transition: 100ms all cubic-bezier(0.12, 0.59, 0.85, 0.99);
    }
    .file-upload:hover span {
        font-size: 7svh;
        transition: 200ms all cubic-bezier(1, 0.39, 0.61, 0.96);
    }
</style>
