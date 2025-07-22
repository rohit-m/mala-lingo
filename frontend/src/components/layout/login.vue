<script setup lang="ts">
import { ref, computed } from 'vue';
import Button from '../ui/Button.vue';
import { useAuthStore } from '../../stores/auth';

const magicword = ref('');

const authStore = useAuthStore();

// Use computed properties to track auth store state
const guestMode = computed(() => authStore.guestMode);
const token = computed(() => authStore.token);

const cancel = () => {
    authStore.guestMode = true;
}

const onSubmit = async () => {
    if (magicword.value) {
        // Check if magicword is correct and set token
        await authStore.checkMagicword(magicword.value);
    }
}
</script>

<template>
    <div class="modal-overlay" v-if="!token && !guestMode">
        <div class="modal-container" data-testid="login-container">
            <h3>Would you like to login?</h3>
            <form class="login-form" data-testid="login-form" @submit.prevent="onSubmit">
                <label for="magicword" data-testid="magicword-label">Where did we go on our first date?</label>
                <input 
                    type="text" 
                    id="magicword" 
                    name="magicword" 
                    data-testid="magicword-input" 
                    v-model="magicword"
                    class="magicword-input"
                />
                <Button label="Login" :data-testid="'login-button'" />
            </form>
            <Button variant="outlined" type="button" label="I dont want to login today." @click="cancel" :data-testid="'cancel-button'" />
        </div>
    </div>
</template>

<style scoped>
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.modal-container {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    max-width: 400px;
    width: 90%;
    text-align: center;
}

.login-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-bottom: 1rem;
}

.login-form label {
    font-size: 1.1rem;
    font-weight: 500;
    color: #333;
    margin-bottom: 0.5rem;
}

.magicword-input {
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
    outline: none;
    transition: border-color 0.2s;
}

.magicword-input:focus {
    border-color: #007bff;
}

.cancel-button {
    width: 100%;
}
</style>
