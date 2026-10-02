(function () {
  function colorScheme() {
    var body = document.querySelector("body");
    return body && body.getAttribute("data-md-color-scheme") === "slate" ? "dark" : "base";
  }

  function makeFiguresReadable() {
    document.querySelectorAll(".mermaid svg").forEach(function (svg) {
      var width = svg.viewBox.baseVal.width;
      if (width > 0) {
        // Keep 20px labels at least 17.5px wide; long diagrams scroll locally.
        svg.style.width = width + "px";
        svg.style.maxWidth = "100%";
        svg.style.minWidth = Math.ceil(width * 0.875) + "px";
      }
      var panel = svg.parentElement;
      panel.tabIndex = 0;
      panel.setAttribute("role", "region");
      panel.setAttribute("aria-label", "教学流程图，宽图可横向滚动查看");
    });
    document.querySelectorAll(".md-content img").forEach(function (img) {
      if (img.closest("a")) return;
      var link = document.createElement("a");
      link.href = img.currentSrc || img.src;
      link.target = "_blank";
      link.rel = "noopener";
      link.className = "figure-original";
      link.title = "打开原图，可放大查看";
      link.setAttribute("aria-label", (img.alt || "教学图") + "，打开原图");
      img.replaceWith(link);
      link.appendChild(img);
    });
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
      theme: colorScheme(),
      fontFamily: '"Noto Sans SC", "Microsoft YaHei", sans-serif',
      themeVariables: {
        fontSize: "20px",
        primaryColor: "#e7f3f0",
        primaryBorderColor: "#39877e",
        primaryTextColor: "#193c37",
        lineColor: "#48736d",
        secondaryColor: "#edf3f8",
        tertiaryColor: "#faf6e9"
      },
      flowchart: { nodeSpacing: 30, rankSpacing: 44, curve: "linear", padding: 16 }
    });
    window.mermaid.run({
      querySelector: ".mermaid[data-mermaid-prepared='true']:not([data-processed='true'])"
    }).then(makeFiguresReadable).catch(function (error) {
      console.error("Mermaid render failed", error);
    });
    makeFiguresReadable();
  }

  if (window.document$) {
    window.document$.subscribe(renderMermaid);
  } else {
    document.addEventListener("DOMContentLoaded", renderMermaid);
  }
})();
