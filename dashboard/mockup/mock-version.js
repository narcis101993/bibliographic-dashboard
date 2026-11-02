(function () {
  "use strict";

  var mockIndex = {
    centralizator: ["v1", "v3"],
    citari: ["v1", "v3"],
    manifest: "dashboard/version-manifest.json",
    manifestDetected: false,
    detectedAt: "31.10.2026 22:04"
  };

  var chip = document.getElementById("versionChip");
  var label = document.getElementById("detectLabel");
  var detail = document.getElementById("detectDetail");
  var path = document.getElementById("detectPath");
  var big = document.getElementById("versionBig");
  var button = document.getElementById("redetect");

  function toNumber(version) {
    return parseInt(String(version).replace(/[^0-9]/g, ""), 10) || 0;
  }

  function commonLatest(index) {
    var groups = [index.centralizator, index.citari];
    var common = groups[0].filter(function (version) {
      return groups.every(function (group) {
        return group.indexOf(version) !== -1;
      });
    });
    if (!common.length) return null;
    common.sort(function (a, b) { return toNumber(a) - toNumber(b); });
    return common[common.length - 1];
  }

  function render(version, note) {
    var safe = version || "—";
    var folders = version
      ? "centralizator/" + version + " · citari/" + version
      : "nicio versiune comună găsită";

    if (chip) chip.textContent = safe;
    if (big) big.textContent = safe;
    if (label) {
      label.textContent = version
        ? "Versiune detectată automat: " + version
        : "Versiune nedetectată";
    }
    if (detail) {
      detail.textContent = folders + " · regulă: versiune semver maximă" + (note ? " · " + note : "");
    }
    if (path) path.textContent = folders;
  }

  function detect(withTimestamp) {
    var version = commonLatest(mockIndex);
    var note = "";
    if (withTimestamp) {
      var now = new Date();
      var pad = function (value) { return String(value).padStart(2, "0"); };
      note = "re-scanat " + pad(now.getHours()) + ":" + pad(now.getMinutes()) + " (simulare)";
    } else {
      note = "manifest " + (mockIndex.manifestDetected ? "găsit" : "absent — fallback pe foldere");
    }
    render(version, note);
  }

  if (button) {
    button.addEventListener("click", function () {
      button.disabled = true;
      button.textContent = "Se scanează…";
      window.setTimeout(function () {
        detect(true);
        button.disabled = false;
        button.textContent = "Re-detectează";
      }, 450);
    });
  }

  detect(false);
})();
