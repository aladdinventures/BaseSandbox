const express = require("express");
const app = express();
const PORT = process.env.PORT || 8000;

app.get("/", (req, res) => res.send("✅ MAMOS Sandbox API is running."));
app.get("/api/health", (req, res) => res.json({ status: "ok", time: new Date() }));

app.listen(PORT, () => console.log(`🚀 Server started on port ${PORT}`));
