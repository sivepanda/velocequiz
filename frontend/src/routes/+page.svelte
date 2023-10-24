<script lang="ts">
    // @ts-nocheck
    import axios, { formToJSON } from "axios";
    import Question from "../components/Question.svelte";

    let files: FileList;

    let questions = []
    $: questions

    const upload = async () => {
        if(!files) {
            console.log('nothing')
            return
        }
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
        questions = response.data
        

        // response.data.forEach(question => {
        //     questions.push(question.replace(/(?:\r\n|\r|\n)/g, '<br>'));
        //     console.log(question)
        // });
        
    }

</script>

<body class="page">
    <h1>Upload new File</h1>
    <label for="avatar">Upload a picture:</label>
    <input accept="pdf" bind:files id="avatar" name="avatar" type="file" />
    <button on:click={upload}>Submit</button>
    
    <div>
        
        <div class="questions">
            <h1>Generated Questions</h1>
            <Question></Question>
            <Question></Question>
            <Question></Question>
            <Question></Question>
            <!-- {#each questions as question}
                {#if question != "null"}
                    <Question question={question}></Question>
                {/if}
            {/each} -->
        </div>
        
    
    </div>
</body>



<style>
    h1 {
        font-size: 5vh;
    }
    .questions {
        margin-left: auto;
        margin-right: auto;
        width: 50vw;
    }

</style>