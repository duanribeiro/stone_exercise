<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Docker Manager</h1>
        <hr><br><br>
        <alert :message=message v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.container-modal>Add Container</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Container ID</th>
              <th scope="col">Image</th>
              <th scope="col">Status Container</th>
              <th scope="col">Options</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(container, index) in containers" :key="index">
              <td>{{ container.id }}</td>
              <td>{{ container.image }}</td>
               <td>{{ container.status_container }}</td>

              <td>
                <div class="btn-group" role="group">
                  <button
                          type="button"
                          class="btn btn-warning btn-sm"
                          @click="onStartContainer(container)">
                      Start
                  </button>
                   <button
                          type="button"
                          class="btn btn-warning btn-sm"
                          @click="onStopContainer(container)">
                      Stop
                  </button>
                  <button
                          type="button"
                          class="btn btn-danger btn-sm"
                          @click="onDeleteContainer(container)">
                      Remove
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addContainerModal"
            id="container-modal"
            title="Add a new container"
            hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-title-group"
                    label="Image Name:"
                    label-for="form-title-input">
          <b-form-input id="form-title-input"
                        type="text"
                        v-model="addContainerForm.image"
                        required
                        placeholder="Enter a valid docker-hub image name">
          </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
        </b-button-group>
      </b-form>
    </b-modal>

  </div>
</template>
<script>
import axios from 'axios';
import Alert from './Alert.vue';
export default {
  data() {
    return {
      containers: [],
      addContainerForm: {
        id: '',
        image: '',
        status_container: ''
      },
      status: '',
      message: '',
      showMessage: false,
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getContainers() {
      const path = 'http://localhost:5000/containers';
      axios.get(path)
        .then((res) => {
          this.containers = res.data.containers;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    addContainer(payload) {
      const path = 'http://localhost:5000/containers';
      axios.post(path, payload)
        .then((res) => {
          this.getContainers();
          this.status = res.data.status;
          
          if (this.status == 'success') {
              this.message = 'Container added!';
              this.showMessage = true;
          }
          else {
              this.message = 'Wrong image name!';
              this.showMessage = true;
          }
        })
        .catch((error) => {
          console.log(error);
          this.getContainers();
        });
    },
    initForm() {
      this.addContainerForm.image = '';
      this.addContainerForm.id = '';
      this.addContainerForm.status_container = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addContainerModal.hide();
 
      const payload = {
        image: this.addContainerForm.image,
      };
      this.addContainer(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addContainerModal.hide();
      this.initForm();
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.initForm();
      this.getContainers();
    },
    removeContainer(containerID) {
      const path = `http://localhost:5000/containers/${containerID}`;
      axios.delete(path)
        .then(() => {
          this.getContainers();
          this.message = 'Container removed!';
          this.showMessage = true;
        })
        .catch((error) => {
          console.error(error);
          this.getContainers();
        });
    },
    onDeleteContainer(container) {
      this.removeContainer(container.id);
    },
    startContainer(containerID) {
      const path = `http://localhost:5000/containers/${containerID}`;
      axios.post(path)
        .then(() => {
          this.getContainers();
          this.message = 'Container Started!';
          this.showMessage = true;
        })
        .catch((error) => {
          console.error(error);
          this.getContainers();
        });
    },
    onStartContainer(container) {
      this.startContainer(container.id);
    },
    stopContainer(containerID) {
      const path = `http://localhost:5000/containers/${containerID}`;
      axios.put(path)
        .then(() => {
          this.getContainers();
          this.message = 'Container Stoped!';
          this.showMessage = true;
        })
        .catch((error) => {
          console.error(error);
          this.getContainers();
        });
    },
    onStopContainer(container) {
      this.stopContainer(container.id);
      this.initForm();
    },


  },
  created() {
    this.getContainers();
  },
};
</script>
