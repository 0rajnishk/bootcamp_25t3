<template>
    <h1>Login</h1>
    <form>
        <input v-model="data.username" type="text" placeholder="username" />
        <input v-model="data.password" type="password" placeholder="password" />
        <button @click="login()" type="submit">login</button>

    </form>
</template>


<script>
import  axios from  'axios';

export default{
    data(){
        return {
            data:{}
        }
    },
    methods: {
        async login(){
            const response = await axios.post('http://127.0.0.1:5000/login', this.data);
            alert(response.data.msg)
            const token = response.data.token;
            localStorage.setItem('token', token);

        }
    }

}
</script>