// const API_KEY = "SUA_API_KEY";

const gallery = document.getElementById("gallery");
const uploadBtn = document.getElementById("uploadBtn");
const fileInput = document.getElementById("fileInput");

uploadBtn.addEventListener("click", async () => {

  const files = fileInput.files;

  if (!files.length) {
    alert("Selecione arquivos");
    return;
  }

  for (const file of files) {

    const formData = new FormData();
    formData.append("file", file);

    try {

      const response = await fetch(`${API_BASE}/upload`, {
        method: "POST",
        // headers: {
        //   "X-API-Key": API_KEY
        // },
        body: formData
      });

      if (!response.ok) {
        throw new Error("Erro upload");
      }

    } catch (err) {
      console.error(err);
      alert(`Erro ao enviar ${file.name}`);
    }
  }

  fileInput.value = "";

  loadFiles();
});

async function loadFiles() {

  gallery.innerHTML = "";

  try {

    const response = await fetch(`${API_BASE}/list`, {
      // headers: {
      //   "X-API-Key": API_KEY
      // }
    });

    const files = await response.json();

    files.forEach(file => {

      const card = document.createElement("div");
      card.classList.add("card");

      let previewElement;

      if (file.mime_type.startsWith("image/")) {

        previewElement = document.createElement("img");
        previewElement.src = file.url;
        previewElement.classList.add("preview");
      }

      else if (file.mime_type.startsWith("video/")) {

        previewElement = document.createElement("video");
        previewElement.src = file.url;
        previewElement.controls = true;
        previewElement.classList.add("preview");
      }

      else {

        previewElement = document.createElement("div");
        previewElement.classList.add("preview");

        previewElement.innerHTML = `
          <div style="
            display:flex;
            align-items:center;
            justify-content:center;
            height:100%;
            font-size:50px;
          ">
            ??
          </div>
        `;
      }

      const info = document.createElement("div");
      info.classList.add("file-info");

      info.innerHTML = `
        <div class="file-name">${file.filename}</div>
      `;

      const deleteBtn = document.createElement("button");
      deleteBtn.innerText = "Excluir";
      deleteBtn.classList.add("delete-btn");

      deleteBtn.addEventListener("click", () => {
        deleteFile(file.id);
      });

      card.appendChild(previewElement);
      card.appendChild(info);
      card.appendChild(deleteBtn);

      gallery.appendChild(card);

    });

  } catch (err) {

    console.error(err);

  }
}

async function deleteFile(id) {

  if (!confirm("Deseja excluir?")) {
    return;
  }

  try {

    const response = await fetch(`${API_BASE}/delete/${id}`, {
      method: "DELETE"
      // headers: {
      //   "X-API-Key": API_KEY
      // }
    });

    if (!response.ok) {
      console.error(`HTTP Error: ${response.status} - ${response.statusText}`)
      throw new Error("Erro delete");
    }

    loadFiles();

  } catch (err) {

    console.error(err);
    alert("Erro ao excluir");

  }
}

loadFiles();