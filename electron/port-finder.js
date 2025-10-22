const net = require('net');

/**
 * Find an available port starting from the given port
 * @param {number} startPort - Port to start checking from
 * @returns {Promise<number>} - Available port number
 */
function findPort(startPort = 8000) {
  return new Promise((resolve, reject) => {
    const server = net.createServer();
    
    server.listen(startPort, '127.0.0.1', () => {
      const port = server.address().port;
      server.close(() => {
        resolve(port);
      });
    });
    
    server.on('error', (err) => {
      if (err.code === 'EADDRINUSE') {
        // Port is in use, try the next one
        if (startPort < 9000) {
          findPort(startPort + 1).then(resolve).catch(reject);
        } else {
          reject(new Error('No available ports found between 8000-9000'));
        }
      } else {
        reject(err);
      }
    });
  });
}

module.exports = findPort;
