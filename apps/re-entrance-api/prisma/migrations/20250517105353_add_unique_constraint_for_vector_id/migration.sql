/*
  Warnings:

  - A unique constraint covering the columns `[vectorId]` on the table `Feature` will be added. If there are existing duplicate values, this will fail.

*/
-- CreateIndex
CREATE UNIQUE INDEX "Feature_vectorId_key" ON "Feature"("vectorId");
