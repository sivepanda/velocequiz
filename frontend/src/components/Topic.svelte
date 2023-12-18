<script lang="ts">
    import { writable } from "svelte/store";

    /** Object that represents an object extracted by AI 
     * @param name Represents the name of the topic
     * @param text Represents all of the text that is covered by the topic
    */
    class ExtractedTopic {
        name: string;
        text: string;
        numQuestions: number;
        constructor(name: string, text: string) {
            this.name = name;
            this.text = text;
            this.numQuestions = 1;
        }
        /** Sets the number of questions per topic */
        setNumQuestion(num: number) {
            num = num >= 0 ? num : this.numQuestions;
            this.numQuestions = num;
            return this;
        }
    }


    export let topicName = "Example topic name";
    export let topicText = "Example topic text";
    export let value = new ExtractedTopic(topicName, topicText); // This object is exported to expose the selected number of questions per topic to the parent page


    let options = [0, 1, 2, 3, 4, 5]; // 1-5 questions for now, maybe change it later to be some fraction of the number of characters

    let defaultValue = 0;

    const topicWritable = writable(new ExtractedTopic(topicName, topicText));


    $: topicWritable.set($topicWritable.setNumQuestion(defaultValue));
    $: value = $topicWritable;

    /** Generates a random number from 0-255 */
    let rand = () => {
        return Math.floor(Math.random() * 255);
    };

    let gradient = `linear-gradient(45deg, rgb(${rand()},${rand()},${rand()}) 0%, rgb(${rand()},${rand()},${rand()}) 100%)`;
</script>

<div class="outer" style="--bkg: {gradient} !important;">
    <div class="topic">
        <h3>{topicName}</h3>
        <select bind:value={defaultValue}>
            {#each options as value}<option {value}>{value} question{value != 1 ? "s" : ""}</option>{/each}
        </select>
    </div>
</div>

<style>
    select {
        appearance: none;
        border: 0;
        border-radius: 20px;
        font-family: var(--body);
        font-size: 2vh;
        outline: 0;
        backdrop-filter: blur(20px);
        width: 80%;
        padding: 0.5rem 25% 0.5rem 5%;
        background: var(--arrow-icon) no-repeat right 0.8em center / 1.4em,
            linear-gradient(to left, var(--arrow-bg) 3em, var(--select-bg) 3em);
        color: white;
        cursor: pointer;
    }
    select::-ms-expand {
        display: none;
    }
    select:focus {
        outline: none;
    }
    select option {
        color: inherit;
        backdrop-filter: blur(20px);
        background-color: rgba(0, 0, 0, 0.897);
        opacity: 0.2;
    }

    .outer {
        --width: 20vw;
        --height: 20vh;
        --bkg: linear-gradient(45deg, #fc466b, #3f5efb);
        --arrow-bg: rgba(117, 117, 117, 0.336);
        --arrow-icon: url(https://upload.wikimedia.org/wikipedia/commons/9/9d/Caret_down_font_awesome_whitevariation.svg);
        --option-bg: rgba(0, 0, 0, 0.2);
        --select-bg: rgba(255, 255, 255, 0.2);
        background: var(--bkg);
        width: var(--width);
        min-height: var(--height);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-items: center;
        justify-content: center;
        border-radius: 10px;
        margin-bottom: 2vh;
        margin-top: 2vh;
    }
    .topic {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-items: center;
        justify-content: center;
        text-align: center;
        border-radius: 10px;
        justify-self: center;
        width: calc(var(--width) - 5px);
        min-height: calc(var(--height) - 5px);
        background-color: rgba(28, 28, 33, 0.87);
    }
</style>
