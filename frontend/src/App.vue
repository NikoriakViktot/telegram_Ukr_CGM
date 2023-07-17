<template>
  <div>
    <h1>My Form</h1>
    <form @submit.prevent="submitForm">
      <div>
        <label>Type Telegram:</label>
        <input type="text" v-model="typeTelegram">
      </div>
      <div>
        <label>Index Station:</label>
        <input type="text" v-model="indexStation">
      </div>
      <div>
        <label>Number Messages:</label>
        <input type="text" v-model="numberMessages">
      </div>
      <div>
        <label>Date Starting Input:</label>
        <input type="text" v-model="dateStartingInput">
      </div>
      <div>
        <label>Date Finish Input:</label>
        <input type="text" v-model="dateFinishInput">
      </div>
      <div>
        <label>Time Starting Input:</label>
        <input type="text" v-model="timeStartingInput">
      </div>
      <div>
        <label>Time Finish Input:</label>
        <input type="text" v-model="timeFinishInput">
      </div>
      <button type="submit">Submit</button>
    </form>
  </div>
</template>

<script>

import axios from 'axios';

axios.defaults.baseURL = 'http://localhost:8000/telegram'

export default {
  name: 'MyApp',
  data() {
    return {
      typeTelegram: '',
      indexStation: '',
      numberMessages: '',
      dateStartingInput: '',
      dateFinishInput: '',
      timeStartingInput: '',
      timeFinishInput: ''
    };
  },
  methods: {
    submitForm() {
      axios.post('/route/post', {
        typeTelegram: this.typeTelegram,
        indexStation: this.indexStation,
        numberMessages: this.numberMessages,
        dateStartingInput: this.dateStartingInput,
        dateFinishInput: this.dateFinishInput,
        timeStartingInput: this.timeStartingInput,
        timeFinishInput: this.timeFinishInput
      })
      .then(response => {
        // handle successful response
        console.log(response.data);
      })
      .catch(error => {
        // handle error
        console.log(error);
      });
    }
  }
};
</script>
