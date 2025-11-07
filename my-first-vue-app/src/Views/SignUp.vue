<template>
    <h1>Signup</h1>
    <form>
        <input v-model="data.username" type="text" placeholder="username" />
        <input v-model="data.email" type="email" placeholder="email" />
        <input v-model="data.phone_number" type="text" placeholder="phone number" />
        <input v-model="data.password" type="password" placeholder="password" />
        <button @click="register()" type="submit">Register</button>
    </form>


</template>

<script>
import axios from 'axios';


export default {

    data() {
        return {
            data1: 'data1 value',
            data: {
                username: '',
                email: '',
                phone_number: '',
                password: ''
            }

        }
    },
    methods: {

        async popAlert() {
            alert('Hello world!' + this.data1)
        },

        async register() {
            const response = await axios.post('http://127.0.0.1:5000/register', this.data);
            console.log(response)
            alert(response.data.msg)
        }


    }

}


</script>
