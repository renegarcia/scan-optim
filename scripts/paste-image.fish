function paste-image
    set -l ts (date +"%Y-%m-%dT%H-%M-%S")
    set -l fname "imagen-$ts.png"

    # Primero intenta wl-paste (Wayland), luego xclip y xsel (X11)
    if type -q wl-paste
        wl-paste --type=image/png > $fname
        or echo "Error: no hay imagen en el portapapeles o fallo al escribir $fname" >&2; return 1
    else if type -q xclip
        xclip -selection clipboard -t image/png -o > $fname
        or echo "Error: no hay imagen en el portapapeles o fallo al escribir $fname" >&2; return 1
    else if type -q xsel
        xsel --clipboard --output --mime-type=image/png > $fname
        or echo "Error: no hay imagen en el portapapeles o fallo al escribir $fname" >&2; return 1
    else
        echo "Error: ninguna herramienta disponible (wl-paste, xclip o xsel)." >&2
        return 2
    end

    echo $fname
end
