.PHONY: run clean release checkall format 
.PHONY: report-unittesting-latest.txt saveolds report-functesting-latest.txt
.DEFAULT: run

SRC_FILES := main.py ./src/horizon.py ./src/interface.py  ./src/functions.py

OUT_DIR := ./out
RESULT_DIR := ./results

release:
	rm -rf $(OUT_DIR)
	mkdir $(OUT_DIR)
	cp -r ./src $(OUT_DIR)
	cp -r ./ui $(OUT_DIR)
	cp main.py $(OUT_DIR)

clean:
	rm -rf ./.pytest_cache
	rm -rf ./.ruff_cache
	rm -rf $(RESULT_DIR)
	rm -rf $(OUT_DIR)
	rm -f report-unittesting-latest.txt
	rm -f report-functesting-latest.txt

run:
	python3 $(OUT_DIR)/main.py

checkall:
	ruff check
	lizard -E duplicate ./src main.py

format:
	pyformat -a --remove-all-unused-imports -i $(SRC_FILES)

report-unittesting-latest.txt:
	./scripts/coverage.sh test_unit.py > $@

report-functesting-latest.txt:
	rm -rf $(RESULT_DIR)
	mkdir $(RESULT_DIR)
	./scripts/coverage.sh test_functional.py > $@
	pytest ./test_functional.py
	cat ./func_buf.txt >> $@
	rm -f func_buf.txt

saveolds:
	./scripts/saveolds.sh
