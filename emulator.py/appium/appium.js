// Increase the default max listeners limit
require('events').EventEmitter.defaultMaxListeners = 20;

// Import the Appium server and start it
const appium = require('appium');
appium.main();
