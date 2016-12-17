'use strict';

var gulp = require("gulp"),//http://gulpjs.com/
    util = require("gulp-util"),//https://github.com/gulpjs/gulp-util
    sass = require("gulp-sass"),//https://www.npmjs.org/package/gulp-sass
    autoprefixer = require('gulp-autoprefixer'),//https://www.npmjs.org/package/gulp-autoprefixer
    rename = require('gulp-rename'),//https://www.npmjs.org/package/gulp-rename
    clean = require('gulp-clean'),
    log = util.log,
    chalk = require('chalk'),
    angularFilesort = require('gulp-angular-filesort'),
    inject = require('gulp-inject'),
    minifyHtml = require('gulp-htmlmin'),
    uglifyJs = require('gulp-uglify'),
    minifyCss = require('gulp-clean-css'),
    filter = require('gulp-filter'),
    flatten = require('gulp-flatten'),
    runSequence = require('run-sequence'),
    concat = require('gulp-concat'),


    // some gulp config values
    project = {
        src: 'src/',
        tmp: 'tmp/',
        dist_static: '../webanimeupdater/ui/static/',
        dist_template: '../webanimeupdater/ui/templates/'
    },

    // list of where our js files come from
    jsFiles = [
        'src/js/*.js',
        'bower_components/**/*.min.js'
    ],

    // list of where our js.map files come from
    jsMapFiles = [
        'bower_components/**/*.map'
    ],

    // list of style files for scss processing
    themeFiles = [
        'src/sass/*.scss',
    ],

    cssFiles = [
        'src/css/*.css',
        'bower_components/**/*.min.css'
    ],

    // look for html files
    htmlFiles = [
        'src/*.html'
    ],

    viewsFiles = [
        'src/views/**/*.html'
    ];

/*******************************
 * MAIN TASKS
 *******************************/
gulp.task('default', ['build']);

// moves everything to the build folder
gulp.task('build', function(callback) {
    runSequence('clean', ['assets', 'sass', 'css', 'fonts', 'js', 'jsMap'], ['html', 'views'], callback);
});

// run the build task, start up a browser, then
// watch the different file locations and execute
// the relevant tasks
gulp.task('serve', ['build'], function() {

    gulp.watch(jsFiles)
        .on('change', function() {
            runSequence(['js', 'jsMap']);
        });


    // watch the scss files in addition to the sass
    gulp.watch(cssFiles)
        .on('change', function() {
            runSequence('css');
        });


    // watch the scss files in addition to the sass
    gulp.watch(themeFiles)
        .on('change', function() {
            runSequence('sass');
        });

    gulp.watch(htmlFiles)
        .on('change', function() {
            runSequence('html');
        });

    gulp.watch(viewsFiles)
        .on('change', function() {
            runSequence('views');
        });
});



/*******************************
 * SUPPORTING TASKS
 *******************************/
// delete our distribution folder
gulp.task('clean', function() {
    return gulp.src([
                project.dist_static,
                project.dist_template,
                project.tmp
            ])
            .pipe(clean({force: true}));
});

// move everything in the assets folder to distribution
gulp.task('assets', function() {
    return gulp
        .src([
            project.src + 'assets/**/*'
        ])
        .pipe(gulp.dest(project.dist_static + 'assets'));
});

gulp.task('sass', function(){
    // log('Generate CSS files ' + (new Date()).toString());
    gulp.src(themeFiles)
        .pipe(sass({
            style: 'expanded'
        }))
        .pipe(autoprefixer("last 3 version","safari 5", "ie 8", "ie 9"))
        .pipe(gulp.dest(project.tmp + 'style/compiled'))
        .pipe(concat("main.css"))
        .pipe(minifyCss({ processImport: true }))
        .pipe(gulp.dest(project.dist_static + 'css'));
});

// move css files over
gulp.task('css', function() {
    return gulp
            .src(cssFiles)
            .pipe(minifyCss({
                processImport: true
            }))
            .pipe(flatten())
            .pipe(gulp.dest(project.dist_static + 'css'));
});

// move js files over
gulp.task('js', function() {
    return gulp
            .src(jsFiles)
            //.pipe(uglifyJs())
            .pipe(flatten())
            .pipe(gulp.dest(project.dist_static + 'js'));
});

// move jsMap files over
gulp.task('jsMap', function() {
    return gulp
            .src(jsMapFiles)
            .pipe(flatten())
            .pipe(gulp.dest(project.dist_static + 'js'));
});

// move our htmls to dist_static folder
gulp.task('html', function() {
    return gulp
        .src(htmlFiles)
        .pipe(inject(gulp.src(project.dist_static + 'css/*.css', {read:false}), {
            ignorePath: '/../webanimeupdater/ui'
        }))
        .pipe(inject(gulp.src(project.dist_static + 'js/*.min.js').pipe(angularFilesort()), {
            ignorePath: '/../webanimeupdater/ui'
        }))
        .pipe(minifyHtml({
            collapseWhitespace: true,
            removeComments: true
        }))
        .pipe(gulp.dest(project.dist_template));
});

// move our views to dist_static folder
gulp.task('views', function() {
    return gulp
        .src(viewsFiles)
        .pipe(minifyHtml({
            collapseWhitespace: true
        }))
        .pipe(gulp.dest(project.dist_static + 'views'));
});


// move our fonts folder
gulp.task('fonts', function() {
    return gulp
        .src([
            'assets/**/*'
        ])
        .pipe(filter('**/*.{eot,ttf,woff}'))
        .pipe(flatten())
        .pipe(gulp.dest(project.dist_static + 'fonts'));
});