'use strict';

var gulp              =   require('gulp'),
    sass              =   require('gulp-sass'),
    gulpAutoprefixer  =   require('gulp-autoprefixer'),
    sassGlob          =   require('gulp-sass-glob'),
    cleanCSSMinify    =   require('gulp-clean-css'),
    rename            =   require('gulp-rename'),
    gzip              =   require('gulp-gzip'),
    notify            =   require('gulp-notify'),
    sourcemaps        =   require('gulp-sourcemaps');

var sassPaths = [
  'who/styles/who/style.scss',
  'who/styles/who/style-rtl.scss'
];
var sass = require('gulp-sass')(require('sass'));
var sassDest = {
  prd: 'who/static/css/prd',
  dev: 'who/static/css/dev'
};


function styles(env) {
  var s = gulp.src(sassPaths);
  var isDev = env === 'dev';

  if (isDev)
    s = s
        .pipe(sourcemaps.init());

    s = s
        .pipe(sassGlob())
        .pipe(sass().on('error', sass.logError))

    if (!isDev)
        s = s
            .pipe(cleanCSSMinify())

    s = s
        .pipe(gulpAutoprefixer())

    if (isDev)
      s = s
          .pipe(sourcemaps.write('/maps'));

      return s
          .pipe(gulp.dest(sassDest[env]))
          .pipe(notify({ message: `Styles task complete: ${env}` }));
}

gulp.task('styles:prd', function() {
  return styles('prd');
});

gulp.task('styles:dev', function() {
  return styles('dev');
});

gulp.task('default', gulp.series('styles:dev','styles:prd'));
