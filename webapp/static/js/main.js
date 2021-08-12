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

// Live Statistics
if (document.querySelector("#statistics")) {
  let elem = document.querySelectorAll(".number")

  fetch("/liveStats")
    .then((response) => response.json())
    .then((data) => {
      for (const [index, [, number]] of Object.entries(Object.entries(data))) {
        elem[3 - index].innerHTML = number
      }
    })
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

  function formSubmit(response) {
    object.querySelector("p").innerHTML = response["message"]
    if (response["status"]) {
      if (response["superuser"]) {
        object.action = "/admin/home"
      }
      object.submit()
    }
  }

  fetch("/authenticate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((resJson) => formSubmit(resJson))

  return false
}

//signup
function signup(object) {
  let formData = new FormData(object)
  object.querySelector("p").innerHTML = "Please Wait"

  const data = {
    username: formData.get("username").trim(),
    email: formData.get("email").trim(),
    nwpassword: formData.get("nwpassword").trim(),
    repassword: formData.get("repassword").trim(),
  }

  function formSubmit(response) {
    function addRequest(data) {
      fetch("/pending", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      })
        .then((response) => response.json())
        .then((resJson) => {
          object.querySelector("p").innerHTML = resJson["message"]
          alert(resJson["message"])
        })
    }
    if (response["status"]) {
      // console.log("CODE :", response["code"]);
      let code = prompt(response["message"])
      if (code == null || code == "") {
        object.querySelector("p").innerHTML = "Cancelled"
      } else {
        if (code.toUpperCase() == response["code"]) {
          addRequest(data)
        } else {
          alert("wrong verification code")
          object.querySelector("p").innerHTML =
            "Wrong Verification Code, Cancelled"
        }
      }
    } else {
      object.querySelector("p").innerHTML = response["message"]
    }
  }

  fetch("/signup", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((resJson) => formSubmit(resJson))

  return false
}

//forgot password
function forgot() {
  let form = document.querySelector("#login_form")
  let formData = new FormData(form)

  if (formData.get("username").trim().length) {
    const url = "/recover/" + formData.get("username").trim()
    form.querySelector("p").innerHTML = "PLease Wait"

    fetch(url)
      .then((response) => response.json())
      .then(
        (resJson) => (form.querySelector("p").innerHTML = resJson["message"])
      )
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

// Send File to Server
function sendFile() {
  const data = { image: imgDataUrl }

  function displayResult(result) {
    document.querySelector("#span1").innerHTML = JSON.stringify(result["covid"])
    document.querySelector("#span2").innerHTML = JSON.stringify(
      result["normal"]
    )
    if (result["result"].endsWith("Negative")) {
      document.querySelector("#span3").style.color = "#00f5d4"
    } else {
      document.querySelector("#span3").style.color = "#e56b6f"
    }
    document.querySelector("#span3").innerHTML = result["result"]

    if (result["status"]) {
      document.querySelector("#saveBtn").style.cursor = "pointer"
      document.querySelector("#saveBtn").disabled = false
    }
  }

  fetch("/test", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((resJson) => displayResult(resJson))

  return false
}

// Disabling Save Button
if (document.querySelector("#saveBtn")) {
  document.querySelector("#saveBtn").style.cursor = "not-allowed"
  document.querySelector("#saveBtn").disabled = true
}

// Post Message
function postMessage(id) {
  const message = document.querySelector("#postContents").value
  const data = {
    message: message.trim(),
  }

  if (data["message"].length) {
    fetch("/post/add/" + id, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((resJson) => {
        alert(resJson["message"])
        window.location.reload()
      })
  }

  return false
}

// Delete Posted Message
function postDelete(id) {
  fetch("/post/delete/" + id)
    .then((response) => response.json())
    .then((resJson) => {
      alert(resJson["message"])
      window.location.reload()
    })

  return false
}

// Update Password
function updatePassword() {
  const oldpassword = document.querySelector("#oldpassword").value
  const nwpassword = document.querySelector("#nwpassword").value
  const repassword = document.querySelector("#repassword").value

  const data = {
    oldpassword: oldpassword,
    nwpassword: nwpassword,
    repassword: repassword,
  }

  fetch("/updatepassword", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((resJson) => {
      window.location.reload()
      alert(resJson["message"])
    })
}
