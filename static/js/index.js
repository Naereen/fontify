$("#submit-all").attr("disabled", true);
$("#submit-all").hide();

Dropzone.options.uploadDropzone = {
  autoProcessQueue: false,
  init: function() {
    var submitButton = document.querySelector("#submit-all");
    myDropzone = this;
    submitButton.addEventListener("click", function() {
      myDropzone.processQueue();
    });

    this.on("error", function(file, errorMessage) {
      $("#upload-file-validation").text(
        "Please upload only jpg, jpeg, png or pdf file less than 20 MB"
      );
      $("#upload-file-validation").addClass("text-danger");
      this.removeAllFiles(file);
      $("#submit-all").hide();
    });

    this.on("addedfile", function() {
      $("#submit-all").show();
      $("#upload-file-validation").text("Upload the scanned template");
      $("#upload-file-validation").removeClass("text-danger");
    });

    this.on("success", function(file, response) {
      window.location =
        "/finish?key=" + response.key + "&fontname=" + response.font_name;
    });

    this.on("maxfilesexceeded", function(file) {
      $("#upload-file-validation").text("Upload the scanned template");
      $("#upload-file-validation").removeClass("text-danger");
      this.removeAllFiles();
      this.addFile(file);
      $("#submit-all").show();
    });
  },
  paramName: "file", // The name that will be used to transfer the file
  maxFilesize: 20, // MB
  maxFiles: 1,
  acceptedFiles: ".png, .jpg, .jpeg, .pdf",
  dictDefaultMessage: "Drop image here<br>or click to upload"
};
