$("#submit-all").attr("disabled", true);
$("#submit-all").hide();

Dropzone.options.uploadDropzone = {
  autoProcessQueue: false,
  init: function() {
    var submitButton = document.querySelector("#submit-all")
        myDropzone = this;
    submitButton.addEventListener("click", function() {
      myDropzone.processQueue();
    });

    this.on("error", function(file, errorMessage) {
      $("#upload-file-validation").text("Please upload only jpg, png or jpeg file");
      $("#upload-file-validation").addClass("alert");
      this.removeAllFiles(file);
      $("#submit-all").hide();
    });

    this.on("addedfile", function() { 
      $("#submit-all").show();
      $("#upload-file-validation").text("Upload the scanned template");
      $("#upload-file-validation").removeClass("alert");
    });

    this.on("success", function(file, response) {
      window.location="/finish?key=" + response.key + "&font-name=" + response.font_name;
    });

    this.on("maxfilesexceeded", function(file) {
      $("#upload-file-validation").text("Upload the scanned template");
      $("#upload-file-validation").removeClass("alert");
      this.removeAllFiles();
      this.addFile(file);
      $("#submit-all").show();
    });

  },
  paramName: "file", // The name that will be used to transfer the file
  maxFilesize: 20, // MB
  maxFiles: 1,
  acceptedFiles: ".png, .jpg, .jpeg",
  dictDefaultMessage: "Drop image here<br>or click to upload"
};