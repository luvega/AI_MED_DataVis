(function () {
  function colorScheme() {
    var body = document.querySelector("body");
    return body && body.getAttribute("data-md-color-scheme") === "slate" ? "dark" : "default";
  }

  function prepareBlocks() {
    document.querySelectorAll("pre.mermaid").forEach(function (block) {
      if (block.dataset.mermaidPrepared === "true") {
        return;
      }
      var code = block.querySelector("code");
      var source = code ? code.textContent : block.textContent;
      var target = document.createElement("div");
      target.className = "mermaid";
      target.textContent = source;
      target.dataset.mermaidPrepared = "true";
      block.replaceWith(target);
    });
  }

  function renderMermaid() {
    if (!window.mermaid) {
      return;
    }
    prepareBlocks();
    window.mermaid.initialize({
      startOnLoad: false,
      securityLevel: "strict",
      theme: colorScheme()
    });
    window.mermaid.run({
      querySelector: ".mermaid[data-mermaid-prepared='true']:not([data-processed='true'])"
    }).catch(function (error) {
      console.error("Mermaid render failed", error);
    });
  }

  if (window.document$) {
    window.document$.subscribe(renderMermaid);
  } else {
    document.addEventListener("DOMContentLoaded", renderMermaid);
  }
})();
