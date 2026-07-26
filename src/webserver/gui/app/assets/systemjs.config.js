/**
 * System configuration for Angular 2 samples
 * Adjust as necessary for your application needs.
 */

(function(global) {

  var plugin = 'bootstrap';

  var config = {
    map: map,
    baseURL: '/gui/',
    packages: packages
  };

  // map tells the System loader where to look for things
  var map = {
    'app': 'app', // 'dist',
    '@angular': 'app/node_modules/@angular',
    'angular2-in-memory-web-api': 'app/node_modules/angular2-in-memory-web-api',
    'rxjs': 'app/node_modules/rxjs',
    'rxjs-compat': 'app/node_modules/rxjs-compat',
    'ng2-charts': 'app/node_modules/ng2-charts/bundles/ng2-charts.umd.js',
    'chart.js': 'app/node_modules/chart.js/dist/Chart.js',
    'lodash': 'app/node_modules/lodash/lodash.js',
    'moment': 'app/node_modules/moment/moment.js',
    'underscore': 'app/node_modules/underscore/underscore.js',
    '@swimlane/ngx-datatable': 'app/node_modules/@swimlane/ngx-datatable/bundles/swimlane-ngx-datatable.umd.js',
    'leaflet': 'app/node_modules/leaflet/dist',
    '@asymmetrik/ngx-leaflet': 'app/node_modules/@asymmetrik/ngx-leaflet/dist/bundles/ngx-leaflet.umd.js',
    '@asymmetrik/ngx-leaflet-draw': 'app/node_modules/@asymmetrik/ngx-leaflet-draw/src/leaflet-draw/leaflet-draw.module.js',
    'ng2-nvd3': 'app/node_modules/ng2-nvd3/build/lib',
    'angular2-modal': 'app/node_modules/angular2-modal',
    'ngx-bootstrap/modal': 'app/node_modules/ngx-bootstrap/modal/bundles/ngx-bootstrap-modal.umd.js',
    'ngx-bootstrap/component-loader': 'app/node_modules/ngx-bootstrap/component-loader/bundles/ngx-bootstrap-component-loader.umd.js',
    'ngx-bootstrap/positioning': 'app/node_modules/ngx-bootstrap/positioning/bundles/ngx-bootstrap-positioning.umd.js',
    'ngx-bootstrap/utils': 'app/node_modules/ngx-bootstrap/utils/bundles/ngx-bootstrap-utils.umd.js',
    'ngx-popover': 'app/node_modules/ngx-popover',
    'survey-angular': 'app/node_modules/survey-angular',
    'ng2-file-upload': 'app/node_modules/ng2-file-upload'
  };

  // packages tells the System loader how to load when no filename and/or no extension
  var packages = {
    'app' : {
      main: 'main.js',
      defaultExtension: 'js'
    },
    'rxjs' : {
      main: 'index.js',
      defaultExtension: 'js'
    },
    'rxjs-compat' : {
      main: 'index.js',
      defaultExtension: 'js'
    },
    'rxjs/operators' : {
      main: 'index.js',
      defaultExtension: 'js'
    },
    'rxjs/internal-compatibility' : {
      main: 'index.js',
      defaultExtension: 'js'
    },
    'angular2-in-memory-web-api' : {
      main: 'index.js',
      defaultExtension: 'js'
    },
    'leaflet' : {
      main: 'leaflet-src.js',
      defaultExtension: 'js'
    },
    '@asymmetrik/ngx-leaflet' : {
      defaultExtension: 'js'
    },
    '@asymmetrik/ngx-leaflet-draw' : {
      defaultExtension: 'js'
    },
    'ng2-charts' : {
      defaultExtension: 'js'
    },
    'ng2-nvd3' : {
      main: "ng2-nvd3.js",
      defaultExtension: "js"
    },
    'angular2-modal' : {
      main: 'bundle/angular2-modal.rollup.umd',
      defaultExtension: 'js'
    },
    'ngx-popover': {
      main: "index.js",
      defaultExtension: "js"
    },
    'survey-angular': {
      main: "survey.angular.js",
      defaultExtension: "js"
    },
    'ng2-file-upload': {
      main: "ng2-file-upload.js",
      defaultExtension: "js"
    }
  };

  var ngPackageNames = [
    'animations',
    'common',
    'compiler',
    'core',
    'forms',
    'http',
    'platform-browser',
    'platform-browser-dynamic',
    'router',
    'router-deprecated',
    'upgrade'
  ];

  // UMD bundles
  map[`angular2-modal/plugins/${plugin}`] = map['angular2-modal'] + `/plugins/${plugin}/bundle`;
  packages[`angular2-modal/plugins/${plugin}`] =  { defaultExtension: 'js', main: `angular2-modal-${plugin}.rollup.umd` };

  // Individual files (~300 requests):
  ngPackageNames.forEach(function (pkgName) {
      // Bundled (~40 requests):
      //packages['@angular/' + pkgName] = { main: pkgName + '.umd.js', defaultExtension: 'js' };

      // Individual files (~300 requests):
      packages['@angular/'+pkgName] = { main: 'index.js', defaultExtension: 'js' };
  });

  // Bundled (~40 requests):
  function packUmd(pkgName) {
    packages['@angular/'+pkgName] = { main: '/bundles/' + pkgName + '.umd.js', defaultExtension: 'js' };
  }

  // Most environments should use UMD; some (Karma) need the individual index files
  var setPackageConfig = System.packageWithIndex ? packIndex : packUmd;

  // Add package entries for angular packages
  ngPackageNames.forEach(setPackageConfig);

  // HttpClient lives under the @angular/common/http sub-path, which needs its
  // own entry distinct from plain @angular/common.
  packages['@angular/common/http'] = { main: '../bundles/common-http.umd.js', defaultExtension: 'js' };

  var config = {
    map: map,
    packages: packages
  };

  System.config(config);
})(this);
