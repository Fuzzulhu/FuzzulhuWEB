extends CharacterBody3D

# --- Variables de Configuración (como en C# o Python) ---
const VELOCIDAD_CORRER = 8.0  # Aumentamos la velocidad para que se sienta como "correr"
const FUERZA_SALTO = 4.5
const FRICCION = 0.25 # Qué tan rápido se detiene al soltar las teclas (0.0 a 1.0)

# Obtenemos la gravedad por defecto del proyecto
var gravedad = ProjectSettings.get_setting("physics/3d/default_gravity")

# --- Variables de Referencia ---
# @onready significa que Godot espera a que el juego cargue para buscar el nodo hijo.
# El símbolo '$' es el atajo para referenciar a tu nodo hijo.
@onready var sprite_visual = $AnimatedSprite3D


func _ready():
	# Aseguramos que arranque la animación Idle por defecto
	sprite_visual.play("default")


func _physics_process(delta):
	# 1. Aplicar Gravedad (Si no está tocando el piso)
	if not is_on_floor():
		velocity.y -= gravedad * delta

	# 2. Manejar Salto (Barra espaciadora por defecto)
	if Input.is_action_just_pressed("ui_accept") and is_on_floor():
		velocity.y = FUERZA_SALTO

	# 3. CAPTURAR ENTRADA DE MOVIMIENTO (Las flechas del teclado o WASD por defecto)
	# Input.get_axis devuelve -1.0 (izquierda), 1.0 (derecha) o 0.0 (quieto)
	var direccion_horizontal = Input.get_axis("ui_left", "ui_right")

	# 4. LÓGICA DE MOVIMIENTO Y ORIENTACIÓN (Flipping)
	if direccion_horizontal:
		# A. Aplicar Velocidad Matemática en el eje X
		velocity.x = direccion_horizontal * VELOCIDAD_CORRER
		
		# B. MANEJAR ORIENTACIÓN VISUAL
		# Si la dirección es positiva (derecha), desactivamos el reflejo horizontal.
		if direccion_horizontal > 0:
			sprite_visual.flip_h = false
		# Si la dirección es negativa (izquierda), activamos el reflejo horizontal.
		else:
			sprite_visual.flip_h = true
			
		# C. (Opcional) CONTROL DE ANIMACIÓN
		# Aquí le diríamos: sprite_visual.play("correr")
		# Pero primero necesitamos el spritesheet de correr.
		
	else:
		# Fricción: Hacemos que la velocidad en X tienda a 0 suavemente si no hay teclas apretadas.
		velocity.x = move_toward(velocity.x, 0, VELOCIDAD_CORRER * FRICCION)
		
		# Si está quieto, volvemos a la animación Idle por defecto.
		# sprite_visual.play("default")

	# 5. Aplicar Movimiento y detectar colisiones automáticamente
	# Esta función es la que hace todo el cálculo matemático para que no atravieses el piso.
	move_and_slide()
