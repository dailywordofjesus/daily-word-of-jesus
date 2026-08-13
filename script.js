/* DAILY WORD OF JESUS — ad logic: responsive, context-aware, gentle.
   Ad codes reproduced EXACTLY as provided; only loading logic is controlled. */
(function () {
"use strict";

/* Mobile menu */
document.addEventListener("DOMContentLoaded", function () {
  var toggle = document.querySelector(".menu-toggle");
  var nav = document.querySelector(".site-nav");
  if (toggle && nav) toggle.addEventListener("click", function () { nav.classList.toggle("open"); });
});

/* Adsterra units (unchanged) */
var ADS = {
  banner_320x50:  { key: "3f02edc11c207579173975af41b50c89", width: 320, height: 50 },
  banner_728x90:  { key: "3330374558e2c8b28d9676727392c341", width: 728, height: 90 },
  banner_160x300: { key: "8f91a9fc974adc1f87f80c77930983ae", width: 160, height: 300 },
  banner_160x600: { key: "d593d1427ad6698224000013f92d7f39", width: 160, height: 600 },
  banner_300x250: { key: "5a3c3da4e25184eebc2a4c9935389788", width: 300, height: 250 },
  banner_468x60:  { key: "f7e68f4292d788ccf9c26dd7bbc71720", width: 468, height: 60 }
};
var POPUNDER_SRC = "https://pl30689879.effectivecpmnetwork.com/97/8d/8d/978d8d9ba093a4f6f77f466bfe9e1cee.js";
var NATIVE_SRC = "https://pl30689878.effectivecpmnetwork.com/59cf4718db1146e6cc7141e8bc580920/invoke.js";
var NATIVE_CONTAINER_ID = "container-59cf4718db1146e6cc7141e8bc580920";
var SOCIAL_BAR_SRC = "https://pl30585186.effectivecpmnetwork.com/29/bc/16/29bc16d9958c6f533c3d2ae86c69d5e6.js";

function injectBanner(containerId, adDef) {
  var container = document.getElementById(containerId);
  if (!container || container.dataset.loaded === "1") return;
  container.dataset.loaded = "1";
  var optsScript = document.createElement("script");
  optsScript.type = "text/javascript";
  optsScript.text =
    "atOptions = {" +
    "'key' : '" + adDef.key + "'," +
    "'format' : 'iframe'," +
    "'height' : " + adDef.height + "," +
    "'width' : " + adDef.width + "," +
    "'params' : {}" +
    "};";
  container.appendChild(optsScript);
  var invokeScript = document.createElement("script");
  invokeScript.src = "https://www.highperformanceformat.com/" + adDef.key + "/invoke.js";
  container.appendChild(invokeScript);
}

function injectResponsiveBanner(containerId, variants) {
  var w = window.innerWidth, key;
  if (w >= 992 && variants.desktop) key = variants.desktop;
  else if (w >= 600 && variants.tablet) key = variants.tablet;
  else key = variants.mobile;
  if (key) injectBanner(containerId, ADS[key]);
}

function injectSidebarBanner(containerId, variant) {
  if (window.innerWidth < 960) return; /* no sidebar ads on mobile */
  injectBanner(containerId, ADS[variant]);
}

function injectNativeBanner(containerId) {
  var container = document.getElementById(containerId);
  if (!container || container.dataset.loaded === "1") return;
  container.dataset.loaded = "1";
  var holder = document.createElement("div");
  holder.id = NATIVE_CONTAINER_ID;
  container.appendChild(holder);
  var script = document.createElement("script");
  script.async = true;
  script.setAttribute("data-cfasync", "false");
  script.src = NATIVE_SRC;
  container.appendChild(script);
}

function loadSocialBar() {
  if (document.body.dataset.socialBarLoaded === "1") return;
  document.body.dataset.socialBarLoaded = "1";
  var script = document.createElement("script");
  script.src = SOCIAL_BAR_SRC;
  document.body.appendChild(script);
}

/* Popunder: max 1x per session, and only after the page fully loads + 3s,
   so it never interrupts the reading moment. */
function loadPopunderOncePerSession() {
  try {
    if (sessionStorage.getItem("dwoj_popunder_shown") === "1") return;
    sessionStorage.setItem("dwoj_popunder_shown", "1");
  } catch (e) {
    if (window.__dwojPopShown) return;
    window.__dwojPopShown = true;
  }
  function attach() {
    var script = document.createElement("script");
    script.src = POPUNDER_SRC;
    document.body.appendChild(script);
  }
  if (document.readyState === "complete") setTimeout(attach, 3000);
  else window.addEventListener("load", function () { setTimeout(attach, 3000); });
}

/* Boot */
document.addEventListener("DOMContentLoaded", function () {
  if (document.getElementById("ad-header")) {
    injectResponsiveBanner("ad-header", {
      desktop: "banner_728x90", tablet: "banner_468x60", mobile: "banner_320x50"
    });
  }
  if (document.getElementById("ad-article-300x250")) injectBanner("ad-article-300x250", ADS.banner_300x250);
  if (document.getElementById("ad-native")) injectNativeBanner("ad-native");
  var sidebarSlot = document.getElementById("ad-sidebar");
  if (sidebarSlot) {
    injectSidebarBanner("ad-sidebar", sidebarSlot.getAttribute("data-variant") || "banner_160x300");
  }
  loadSocialBar();
  loadPopunderOncePerSession();

  var resizeTimer;
  window.addEventListener("resize", function () {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function () {
      var el = document.getElementById("ad-sidebar");
      if (el) injectSidebarBanner("ad-sidebar", el.getAttribute("data-variant") || "banner_160x300");
    }, 300);
  });
});
})();