import { writable } from 'svelte/store';
import { browser } from '$app/environment';

const localStorageKey = 'createdQuizzes';

const storedQuizzes = browser && localStorage.getItem(localStorageKey);
export const quizzes = writable(storedQuizzes);
quizzes.subscribe((value) => {
    browser && value ? localStorage.setItem(localStorageKey, value) : '';
});
