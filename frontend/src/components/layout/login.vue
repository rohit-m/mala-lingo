<script setup lang="ts">
import { ref } from 'vue';
import Button from '../ui/Button.vue';
import { useAuthStore } from '../../stores/auth';

const magicword = ref('');

const authStore = useAuthStore();

const cancel = () => {
    console.log('cancel');
    magicword.value = '';
}

const onSubmit = async () => {
    if (magicword.value) {
        // Check if magicword is correct and set token
        await authStore.checkMagicword(magicword.value);
    }
}
</script>

<template v-if="!authStore.token">
    <div data-testid="login-container">
        <form data-testid="login-form">
            <label for="magicword" data-testid="magicword-label">Where did we go on our first date?</label>
            <input type="text" id="magicword" name="magicword" data-testid="magicword-input" v-model="magicword" />
            <Button type="submit" label="Login" @click="onSubmit" :data-testid="'login-button'" />
        </form>
        <Button type="button" label="I dont want to login today." @click="cancel" :data-testid="'cancel-button'" />
    </div>
</template>
