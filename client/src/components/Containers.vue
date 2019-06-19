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
              <th scope="col">Options</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(container, index) in containers" :key="index">
              <td>{{ container.id }}</td>
              <td>{{ container.image }}</td>

              <td>
                <div class="btn-group" role="group">
                  <button
                          type="button"
                          class="btn btn-warning btn-sm"
                          v-b-modal.book-update-modal
                          @click="editBook(book)">
                      Start
                  </button>
                   <button
                          type="button"
                          class="btn btn-warning btn-sm"
                          v-b-modal.book-update-modal
                          @click="editBook(book)">
                      Stop
                  </button>
                  <button
                          type="button"
                          class="btn btn-danger btn-sm"
                          @click="onDeleteBook(container)">
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
    <b-modal ref="editBookModal"
            id="book-update-modal"
            title="Update"
            hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
      <b-form-group id="form-title-edit-group"
                    label="Title:"
                    label-for="form-title-edit-input">
          <b-form-input id="form-title-edit-input"
                        type="text"
                        v-model="editForm.title"
                        required
                        placeholder="Enter title">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-author-edit-group"
                      label="Author:"
                      label-for="form-author-edit-input">
            <b-form-input id="form-author-edit-input"
                          type="text"
                          v-model="editForm.author"
                          required
                          placeholder="Enter author">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-read-edit-group">
          <b-form-checkbox-group v-model="editForm.read" id="form-checks">
            <b-form-checkbox value="true">Read?</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Update</b-button>
          <b-button type="reset" variant="danger">Cancel</b-button>
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
        image: '',
      },
      status: '',
      message: '',
      showMessage: false,
      editForm: {
        id: '',
        title: '',
        author: '',
        read: [],
      },
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
      this.addContainerForm.title = '';
      this.addContainerForm.author = '';
      this.addContainerForm.read = [];
      this.editForm.id = '';
      this.editForm.title = '';
      this.editForm.author = '';
      this.editForm.read = [];
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

    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editBookModal.hide();
      let read = false;
      if (this.editForm.read[0]) read = true;
      const payload = {
        title: this.editForm.title,
        author: this.editForm.author,
        read,
      };
      this.updateBook(payload, this.editForm.id);
    },
    updateBook(payload, containerID) {
      const path = `http://localhost:5000/containers/${containerID}`;
      axios.put(path, payload)
        .then(() => {
          this.getContainers();
          this.message = 'Book updated!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getContainers();
        });
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editBookModal.hide();
      this.initForm();
      this.getContainers(); // why?
    },
    removeContainer(containerID) {
      const path = `http://localhost:5000/containers/${containerID}`;
      axios.delete(path)
        .then(() => {
          this.getContainers();
          this.message = 'Book removed!';
          this.showMessage = true;
        })
        .catch((error) => {
          console.error(error);
          this.getContainers();
        });
    },
    onDeleteBook(container) {
      this.removeContainer(container.id);
    },
  },
  created() {
    this.getContainers();
  },
};
</script>
