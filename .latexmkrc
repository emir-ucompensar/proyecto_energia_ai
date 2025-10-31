# === Configuración de Latexmk para proyecto_energia_ai ===

# Directorios de salida y auxiliares
$out_dir = 'build';
$aux_dir = 'build';

# Modo de compilación: PDF
$pdf_mode = 1;

# Número de veces para ejecutar pdflatex antes y después de bibtex
$max_repeat = 5;

# Configuración de comandos
$pdflatex = 'pdflatex -interaction=nonstopmode -file-line-error -synctex=1';
$bibtex = "bibtex";

# Agrega los directorios de búsqueda para archivos
$ENV{'TEXINPUTS'} = './/:' . ($ENV{'TEXINPUTS'} || '');
$ENV{'BIBINPUTS'} = './/:' . ($ENV{'BIBINPUTS'} || '');
$ENV{'BSTINPUTS'} = './/:' . ($ENV{'BSTINPUTS'} || '');

# Fuerza el uso de bibtex
$bibtex_use = 1.5;

# Extensiones de archivos a limpiar
$clean_ext = 'bbl nav out snm aux dvi log ps aux log bbl blg toc synctex.gz run.xml bcf fdb_latexmk fls';

# Reconstruir si los archivos han cambiado
$force_mode = 1;
