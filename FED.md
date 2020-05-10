WHO APP UPDATE

Run the Django app as per README.rst 
Open a new terminal window to: CMD to local project - run 'node install' to download package.json.
Add styles changes on `styles/who/**/*` - run `gulp` command once you have applied all SASS changes.



FED
  Maintenance, Performance, and Readability.

  MARKUP & CSS
  ---------------
  -  We use SMACSS, BEM methodologies

  BEM
  https://en.bem.info/methodology/quick-start/
  http://getbem.com/introduction/

  BEM Naming Convention
    Languages
    Language__current
    Language__title
    Language__title--icon
    Language__dropdown-button

    Language__list
    Language-list__toggle
    Language-list__item

  SMACSS
  https://smacss.com/book/

  E.G. variables / colors.scss
    $de_york - #2A9B58;
    $robin_egg_blue - #37BFBE;
    $mandy - #EC3B3A;
    $danube - #5F7AC9;
    $roman - #EF9955;
    $saffron - #F2B438;
    $medium_violet - #B62A99;

  FILE PATH: /styles/app-name/
    /layout/
      _l-header.scss
      _l-footer.scss
      _l-layout.scss | @import all layout compoments
    /modules
      _m-article-list.scss
      _m-article.scss
      _m-modules.scss | @import all modules compoments
    /state
      _s-article-list.scss
      _s-article.scss
      _s-state.scss | @import all state compoments
    /variables
      variables.scss
      color.scss
    _base.scss
    _versions.scss
    styles.scss | @import all compoments
    styles-rtl.scss

  OUTPUT FILE PATH: /static/css/dev with sourcemaps /maps
                    /static/css/prd


  CSS / BEM Linting
  https://github.com/postcss/postcss-bem-linter
  - Enforce coding standard rules


  COMPRESSION / AUTOMATION
  -------------------------
  Requirements:
  Must have node.js npm and gulp installed globally

  - npm install gulp-cli -g

  For asset bundling & processing, concatenating and minification file:
  - gulpfile.js
  - package.json

  Commands:
  - npm install
  - gulp

  IMAGES FORMATS:
    SVG, PNG, Sprites icons
    Images must be compressed
