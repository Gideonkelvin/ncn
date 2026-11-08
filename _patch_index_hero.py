from pathlib import Path

p = Path("templates/index.html")
text = p.read_text(encoding="utf-8")
start = text.index('        <motion.div class="owl-carousel header-carousel')
start = text.index('        <motion.div class="owl-carousel header-carousel')
start = text.index('        <div class="owl-carousel header-carousel')
end = text.index("    </div>\n    <!-- Carousel End -->")
new_block = """        <div class="owl-carousel header-carousel header-carousel--fade position-relative">
            {% for slide in home_hero_slides %}
            <div class="owl-carousel-item position-relative">
                <img class="img-fluid" src="{{ slide.image.url }}" alt="" loading="{% if forloop.first %}eager{% else %}lazy{% endif %}" decoding="async">
                {% include 'includes/home_hero_slide_overlay.html' %}
            </div>
            {% empty %}
            <div class="owl-carousel-item position-relative">
                <img class="img-fluid" src="{% static 'img/carousel-1.jpg' %}" alt="" loading="eager" decoding="async">
                {% include 'includes/home_hero_slide_overlay.html' %}
            </div>
            <div class="owl-carousel-item position-relative">
                <img class="img-fluid" src="{% static 'img/carousel-2.jpg' %}" alt="" loading="lazy" decoding="async">
                {% include 'includes/home_hero_slide_overlay.html' %}
            </div>
            <div class="owl-carousel-item position-relative">
                <img class="img-fluid" src="{% static 'img/carousel-3.jpg' %}" alt="" loading="lazy" decoding="async">
                {% include 'includes/home_hero_slide_overlay.html' %}
            </div>
            {% endfor %}
        </div>
"""
p.write_text(text[:start] + new_block + text[end:], encoding="utf-8")
print("patched")
