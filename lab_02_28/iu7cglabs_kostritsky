.PHONY: run clean release checkall format report-unittesting-latest.txt saveolds

.DEFAULT: release

OUT_DIR := ./out

release:
	rm -rf $(OUT_DIR)
	mkdir $(OUT_DIR)
	cp -r ./src $(OUT_DIR)
	cp main.py $(OUT_DIR)

clean:
	rm -rf ./.pytest_cache
	rm -rf ./.ruff_cache
	rm -rf $(OUT_DIR)
	rm -f report-unittesting-latest.txt

run:
	python3 $(OUT_DIR)/main.py

checkall:
	ruff check
	lizard -E duplicate

format:
	pyformat -i main.py ./src/circle.py ./src/interface.py \
	./src/maxarea.py ./src/widgets.py

report-unittesting-latest.txt:
	./scripts/coverage.sh > $@

saveolds:
	./scripts/saveolds.sh
