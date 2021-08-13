// Messsage Button
if (document.querySelector("#message")) {
  document.querySelector("#message").addEventListener("click", () => {
    document.querySelector("#messages").classList.toggle("show")
    document.querySelector("#message").classList.toggle("icon-active")
  })
}

// Navigation Hilight
var navState = document.querySelector("#" + document.title.toLowerCase())
if (navState) {
  navState.classList.add("item-active")
}

// Display Clock
if ((time = document.querySelector("#clockTime"))) {
  function displayClock() {
    var display = new Date().toLocaleTimeString()
    time.innerHTML = display
    setTimeout(displayClock, 1000)
  }
  displayClock()
}

// Card Comments
function commentDrop(elem) {
  var attr = window.getComputedStyle(elem, null).getPropertyValue("transform")
  yPosition = attr.slice(attr.lastIndexOf(",") + 1, attr.indexOf(")"))

  if (!parseInt(yPosition)) {
    elem.style.transform = "translateY(-265px)"
    elem.querySelector("#arrow-btn").style.transform =
      "translateX(-50%) rotate(0deg)"
  } else {
    elem.style.transform = "translateY(0)"
    elem.querySelector("#arrow-btn").style.transform =
      "translateX(-50%) rotate(180deg)"
  }
}

//login
function login(object) {
  let formData = new FormData(object)

  const data = {
    username: formData.get("username").trim(),
    password: formData.get("password").trim(),
  }
  if (data.username == "root" && data.password == "root") {
    object.querySelector("p").innerHTML = "Login Successful"
    window.location.replace("home.html")
  } else {
    object.querySelector("p").innerHTML = "Username : root | Password : root"
  }

  return false
}

//forgot password
function forgot() {
  let form = document.querySelector("#login_form")
  let formData = new FormData(form)

  if (formData.get("username").trim().length) {
    form.querySelector("p").innerHTML = "Username : root | Password : root"
  } else {
    alert("Please Provide a User Name")
  }
}

// Character Count Update
function updateCharCount(value) {
  count = document.querySelector("#charcount")
  count.innerHTML = value.length
}

// Image URL Generation
function getDataUrl(img) {
  const canvas = document.createElement("canvas")
  const ctx = canvas.getContext("2d")
  canvas.width = img.naturalWidth
  canvas.height = img.naturalHeight
  ctx.drawImage(img, 0, 0)
  return canvas.toDataURL("image/png")
}

// Select the image
const img = document.querySelector("#show")
var imgDataUrl = undefined

if (img) {
  img.addEventListener("load", function (event) {
    const dataUrl = getDataUrl(event.currentTarget)
    imgDataUrl = dataUrl
  })
}

// Disabling Save Button
if (document.querySelector("#saveBtn")) {
  document.querySelector("#saveBtn").style.cursor = "not-allowed"
  document.querySelector("#saveBtn").disabled = true
}
