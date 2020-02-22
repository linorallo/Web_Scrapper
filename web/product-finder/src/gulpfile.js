
//dependencies
const gulp = require('gulp');
const sass = require('gulp-sass');
const plumber = require('gulp-plumber');
const postcss = require('gulp-postcss');
const rename =  require('gulp-rename');
const autoprefixer =  require('autoprefixer');
const cssnano = require("cssnano");
const browsersync = require('browser-sync').create();
var SCSS_SRC = './src/Assets/scss/**/*.scss';
var SCSS_DEST = './src/Assets/css2';
function style(){
    return gulp
    .src("./Assets/scss/**/*.scss")
    .pipe(plumber())
    .pipe(sass({ outputStyle: "expanded" }))
    .pipe(gulp.dest("./Assets/css/"))
    .pipe(rename({ suffix: ".min" }))
    .pipe(postcss([autoprefixer(), cssnano()]))
    .pipe(gulp.dest("./Assets/css/"))
    .pipe(browsersync.stream());
}
exports.style = style;


